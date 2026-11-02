import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = process.env.PORT || 3000;

const MIME_TYPES = {
  '.html': 'text/html; charset=UTF-8',
  '.css': 'text/css; charset=UTF-8',
  '.js': 'application/javascript; charset=UTF-8',
  '.json': 'application/json; charset=UTF-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

import { 
  testMongoConnection, 
  getAllStudentsFromMongo, 
  saveStudentToMongo, 
  deleteStudentFromMongo, 
  syncAllStudentsToMongo 
} from './mongodb-atlas.js';

function sendJson(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=UTF-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  });
  res.end(JSON.stringify(data));
}

function parseJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 5 * 1024 * 1024) { // 5MB limit
        reject(new Error("Request body too large"));
      }
    });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        reject(new Error("Invalid JSON body"));
      }
    });
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    });
    res.end();
    return;
  }

  // =========================================================
  // MONGODB ATLAS API ROUTES
  // =========================================================
  const urlObj = new URL(req.url, `http://${req.headers.host || 'localhost:3000'}`);
  const pathname = urlObj.pathname;

  if (pathname.startsWith('/api/mongodb')) {
    try {
      if (pathname === '/api/mongodb/test' && req.method === 'POST') {
        await parseJsonBody(req);
        const result = await testMongoConnection();
        return sendJson(res, 200, result);
      }

      if (pathname === '/api/mongodb/students' && req.method === 'GET') {
        const students = await getAllStudentsFromMongo();
        return sendJson(res, 200, students || []);
      }

      if (pathname === '/api/mongodb/student' && req.method === 'POST') {
        const student = await parseJsonBody(req);
        if (!student.id) {
          return sendJson(res, 400, { success: false, error: "Student ID is required" });
        }
        const result = await saveStudentToMongo(student);
        return sendJson(res, 200, { success: true, result });
      }

      if (pathname === '/api/mongodb/student' && req.method === 'DELETE') {
        let studentId = urlObj.searchParams.get('id');
        if (!studentId) {
          const body = await parseJsonBody(req).catch(() => ({}));
          studentId = body.id;
        }
        if (!studentId) {
          return sendJson(res, 400, { success: false, error: "Student ID is required" });
        }
        const result = await deleteStudentFromMongo(studentId);
        return sendJson(res, 200, { success: true, result });
      }

      if (pathname === '/api/mongodb/sync' && req.method === 'POST') {
        const body = await parseJsonBody(req);
        const students = Array.isArray(body) ? body : (body.students || []);
        const result = await syncAllStudentsToMongo(students);
        return sendJson(res, 200, { success: true, result });
      }

      return sendJson(res, 404, { success: false, error: "Endpoint not found" });
    } catch (err) {
      console.error("MongoDB API error:", err);
      return sendJson(res, 500, { success: false, error: err.message || "Internal server error" });
    }
  }

  // Normalize URL path to prevent directory traversal
  let safePath = path.normalize(decodeURI(req.url.split('?')[0])).replace(/^(\.\.[\/\\])+/, '');
  if (safePath === '/' || safePath === '\\') {
    safePath = '/index.html';
  }

  const filePath = path.join(__dirname, safePath);

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      // Fallback to index.html
      const indexPath = path.join(__dirname, 'index.html');
      fs.readFile(indexPath, (readErr, content) => {
        if (readErr) {
          res.writeHead(404, { 'Content-Type': 'text/plain' });
          res.end('404 Not Found');
        } else {
          res.writeHead(200, { 'Content-Type': 'text/html; charset=UTF-8' });
          res.end(content);
        }
      });
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    fs.readFile(filePath, (readErr, content) => {
      if (readErr) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('500 Server Error');
        return;
      }
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    });
  });
});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
