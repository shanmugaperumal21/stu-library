import { getApps, initializeApp } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';
import { onRequest } from 'firebase-functions/v2/https';
import { defineSecret } from 'firebase-functions/params';
import { MongoClient, ServerApiVersion } from 'mongodb';

if (getApps().length === 0) {
  initializeApp();
}

const mongodbUri = defineSecret('MONGODB_URI');
const dbName = 'studentsphere_db';
const collectionName = 'students';

let mongoClient;
let mongoConnection;
let mongoConnectionPromise;

async function getMongoDatabase() {
  const uri = mongodbUri.value();
  if (!uri) {
    throw new Error('MongoDB Atlas is not configured on the server.');
  }

  if (mongoClient && mongoConnection) {
    return mongoConnection;
  }
  if (mongoConnectionPromise) {
    return mongoConnectionPromise;
  }

  const client = new MongoClient(uri, {
    serverApi: {
      version: ServerApiVersion.v1,
      strict: false,
      deprecationErrors: true
    },
    serverSelectionTimeoutMS: 8000,
    connectTimeoutMS: 8000
  });

  mongoConnectionPromise = client.connect()
    .then(() => {
      mongoClient = client;
      mongoConnection = client.db(dbName);
      return mongoConnection;
    })
    .catch(async (error) => {
      await client.close().catch(() => {});
      mongoConnectionPromise = null;
      throw error;
    });

  return mongoConnectionPromise;
}

function normalizeStudent(student) {
  if (!student || typeof student !== 'object' || Array.isArray(student) || !student.id) {
    throw new Error('Each student must have an ID.');
  }

  return {
    id: String(student.id),
    name: String(student.name || ''),
    age: Number.parseInt(student.age, 10) || 20,
    department: String(student.department || ''),
    updatedAt: new Date().toISOString()
  };
}

async function verifyFirebaseUser(req) {
  const authorization = req.get('authorization') || '';
  const token = authorization.startsWith('Bearer ')
    ? authorization.slice('Bearer '.length)
    : '';

  if (!token) {
    throw new Error('Authentication is required.');
  }

  await getAuth().verifyIdToken(token);
}

export const mongodbApi = onRequest(
  { region: 'us-central1', secrets: [mongodbUri], timeoutSeconds: 30 },
  async (req, res) => {
    if (req.method === 'OPTIONS') {
      return res.status(204).end();
    }

    try {
      await verifyFirebaseUser(req);
    } catch {
      return res.status(401).json({ success: false, error: 'Please sign in with Firebase to access MongoDB.' });
    }

    try {
      const bodySize = Buffer.byteLength(JSON.stringify(req.body || {}));
      if (bodySize > 5 * 1024 * 1024) {
        return res.status(413).json({ success: false, error: 'Request body too large.' });
      }

      const requestPath = req.path.startsWith('/api/mongodb/')
        ? req.path.slice('/api/mongodb'.length)
        : req.path;

      if (requestPath === '/test' && req.method === 'POST') {
        const db = await getMongoDatabase();
        await db.command({ ping: 1 });
        return res.status(200).json({
          success: true,
          message: `Successfully connected to MongoDB Atlas database "${dbName}"!`,
          dbName,
          ping: true
        });
      }

      if (requestPath === '/students' && req.method === 'GET') {
        const collection = (await getMongoDatabase()).collection(collectionName);
        const records = await collection.find({}, { projection: { _id: 0 } }).toArray();
        return res.status(200).json(records);
      }

      if (requestPath === '/student' && req.method === 'POST') {
        const student = normalizeStudent(req.body);
        const collection = (await getMongoDatabase()).collection(collectionName);
        const result = await collection.updateOne(
          { id: student.id },
          { $set: student },
          { upsert: true }
        );
        return res.status(200).json({ success: true, result });
      }

      if (requestPath === '/student' && req.method === 'DELETE') {
        const studentId = String(req.query.id || '');
        if (!studentId) {
          return res.status(400).json({ success: false, error: 'Student ID is required.' });
        }

        const collection = (await getMongoDatabase()).collection(collectionName);
        const result = await collection.deleteOne({ id: studentId });
        return res.status(200).json({ success: true, result });
      }

      if (requestPath === '/sync' && req.method === 'POST') {
        const records = Array.isArray(req.body)
          ? req.body
          : req.body && Array.isArray(req.body.students)
            ? req.body.students
            : null;
        if (!records) {
          return res.status(400).json({ success: false, error: 'Students must be an array.' });
        }

        const collection = (await getMongoDatabase()).collection(collectionName);
        const operations = records.map((record) => {
          const student = normalizeStudent(record);
          return {
            updateOne: {
              filter: { id: student.id },
              update: { $set: student },
              upsert: true
            }
          };
        });

        if (operations.length > 0) {
          await collection.bulkWrite(operations);
        }
        return res.status(200).json({ success: true, result: { count: operations.length } });
      }

      return res.status(404).json({ success: false, error: 'Endpoint not found.' });
    } catch (error) {
      console.error('MongoDB API request failed:', error);
      return res.status(500).json({ success: false, error: 'MongoDB request failed. Check the server configuration and logs.' });
    }
  }
);
