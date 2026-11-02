// MongoDB Atlas Node.js Driver Integration
// Uses official 'mongodb' package to connect directly to your MongoDB Atlas cluster.
import { MongoClient, ServerApiVersion } from 'mongodb';
import { getActiveMongoConfig, isMongoConfigured } from './mongodb-config.js';

let cachedClient = null;
let cachedDb = null;
let activeUriUsed = null;
let activeDbNameUsed = null;

/**
 * Timeout helper for DB operations
 */
function withTimeout(promise, ms = 6000) {
  let timeoutId;
  const timeoutPromise = new Promise((_, reject) => {
    timeoutId = setTimeout(() => {
      reject(new Error("Timeout connecting to MongoDB Atlas cluster (check your Network Access IP whitelist)"));
    }, ms);
  });
  return Promise.race([
    promise.finally(() => clearTimeout(timeoutId)),
    timeoutPromise
  ]);
}

/**
 * Connects to MongoDB Atlas cluster or returns cached DB connection
 */
export async function getMongoDb(customConfig = null) {
  const config = customConfig || getActiveMongoConfig();
  if (!config || !config.uri || config.uri === 'YOUR_MONGODB_ATLAS_URI') {
    return null;
  }

  const uri = config.uri.trim();
  const dbName = (config.dbName || 'studentsphere_db').trim();

  // Return cached DB if configuration hasn't changed and client is open
  if (cachedClient && cachedDb && activeUriUsed === uri && activeDbNameUsed === dbName) {
    return cachedDb;
  }

  // Close previous client if URI changed
  if (cachedClient) {
    try {
      await cachedClient.close();
    } catch (e) {
      // ignore
    }
    cachedClient = null;
    cachedDb = null;
  }

  const client = new MongoClient(uri, {
    serverApi: {
      version: ServerApiVersion.v1,
      strict: false,
      deprecationErrors: true
    },
    serverSelectionTimeoutMS: 5000,
    connectTimeoutMS: 5000
  });

  await withTimeout(client.connect(), 6000);
  const db = client.db(dbName);

  cachedClient = client;
  cachedDb = db;
  activeUriUsed = uri;
  activeDbNameUsed = dbName;

  return db;
}

/**
 * Tests connection to MongoDB Atlas cluster
 */
export async function testMongoConnection(customUri = null, customDbName = null) {
  const config = getActiveMongoConfig();
  const uri = (customUri || config.uri || '').trim();
  const dbName = (customDbName || config.dbName || 'studentsphere_db').trim();

  if (!uri || uri === 'YOUR_MONGODB_ATLAS_URI') {
    throw new Error("MongoDB Atlas URI is not configured yet. Please provide a valid mongodb+srv:// connection string.");
  }

  if (uri.includes('<password>')) {
    throw new Error("Please replace '<password>' in your connection string with your actual Atlas database user password.");
  }

  let tempClient = null;
  try {
    tempClient = new MongoClient(uri, {
      serverApi: {
        version: ServerApiVersion.v1,
        strict: false,
        deprecationErrors: true
      },
      serverSelectionTimeoutMS: 6000,
      connectTimeoutMS: 6000
    });

    await withTimeout(tempClient.connect(), 7000);
    const db = tempClient.db(dbName);
    const pingResult = await db.command({ ping: 1 });

    return {
      success: true,
      message: `Successfully connected to MongoDB Atlas database "${dbName}"!`,
      dbName,
      ping: pingResult.ok === 1
    };
  } catch (err) {
    console.error("MongoDB Atlas connection test error:", err);
    let msg = err.message || String(err);
    if (msg.includes('bad auth') || msg.includes('Authentication failed')) {
      msg = "Authentication failed: Please check your MongoDB Atlas username and password in the connection string.";
    } else if (msg.includes('whitelist') || msg.includes('timed out') || msg.includes('Server selection')) {
      msg = "Connection timed out: In MongoDB Atlas, go to Network Access -> Add IP Address -> Select 'Allow Access from Anywhere' (0.0.0.0/0).";
    }
    throw new Error(msg);
  } finally {
    if (tempClient) {
      tempClient.close().catch(() => { });
    }
  }
}

/**
 * Retrieves all students from MongoDB Atlas
 */
export async function getAllStudentsFromMongo(customConfig = null) {
  try {
    const db = await getMongoDb(customConfig);
    if (!db) return null;

    const config = customConfig || getActiveMongoConfig();
    const colName = config.collectionName || 'students';
    const collection = db.collection(colName);

    const students = await collection.find({}, { projection: { _id: 0 } }).toArray();
    return students;
  } catch (err) {
    console.warn("⚠️ MongoDB Atlas fetch warning:", err.message);
    return null;
  }
}

/**
 * Saves/upserts a student in MongoDB Atlas
 */
export async function saveStudentToMongo(student, customConfig = null) {
  try {
    const db = await getMongoDb(customConfig);
    if (!db) return null;

    const config = customConfig || getActiveMongoConfig();
    const colName = config.collectionName || 'students';
    const collection = db.collection(colName);

    const doc = {
      id: student.id,
      name: student.name,
      age: parseInt(student.age, 10) || 20,
      department: student.department,
      updatedAt: new Date().toISOString()
    };

    const res = await collection.updateOne(
      { id: student.id },
      { $set: doc },
      { upsert: true }
    );

    console.log(`🍃 Synced student ${student.id} to MongoDB Atlas (${colName})!`);
    return { success: true, result: res };
  } catch (err) {
    console.warn("⚠️ MongoDB Atlas save warning:", err.message);
    return null;
  }
}

/**
 * Deletes a student from MongoDB Atlas
 */
export async function deleteStudentFromMongo(studentId, customConfig = null) {
  try {
    const db = await getMongoDb(customConfig);
    if (!db) return null;

    const config = customConfig || getActiveMongoConfig();
    const colName = config.collectionName || 'students';
    const collection = db.collection(colName);

    const res = await collection.deleteOne({ id: studentId });
    console.log(`🍃 Deleted student ${studentId} from MongoDB Atlas (${colName})!`);
    return { success: true, result: res };
  } catch (err) {
    console.warn("⚠️ MongoDB Atlas delete warning:", err.message);
    return null;
  }
}

/**
 * Bulk syncs an array of students to MongoDB Atlas
 */
export async function syncAllStudentsToMongo(students, customConfig = null) {
  if (!Array.isArray(students)) return null;
  try {
    const db = await getMongoDb(customConfig);
    if (!db) return null;

    const config = customConfig || getActiveMongoConfig();
    const colName = config.collectionName || 'students';
    const collection = db.collection(colName);

    // Upsert all student documents
    const operations = students.map(s => ({
      updateOne: {
        filter: { id: s.id },
        update: {
          $set: {
            id: s.id,
            name: s.name,
            age: parseInt(s.age, 10) || 20,
            department: s.department,
            updatedAt: new Date().toISOString()
          }
        },
        upsert: true
      }
    }));

    if (operations.length > 0) {
      await collection.bulkWrite(operations);
      console.log(`🍃 Synced ${operations.length} students to MongoDB Atlas (${colName})!`);
    }

    return { success: true, count: operations.length };
  } catch (err) {
    console.warn("⚠️ MongoDB Atlas bulk sync warning:", err.message);
    return null;
  }
}
