// MongoDB Atlas Frontend Service
// Bridges browser operations with MongoDB Atlas via authenticated HTTP endpoints.
import { getFirebaseAuth } from './auth-service.js';

const API_BASE = (typeof window !== 'undefined' && window.location && window.location.origin) 
  ? window.location.origin 
  : 'http://localhost:3000';

/**
 * Timeout helper for fetch calls
 */
function withTimeout(promise, ms = 5000) {
  let timeoutId;
  const timeoutPromise = new Promise((_, reject) => {
    timeoutId = setTimeout(() => {
      reject(new Error("Timeout contacting MongoDB service"));
    }, ms);
  });
  return Promise.race([
    promise.finally(() => clearTimeout(timeoutId)),
    timeoutPromise
  ]);
}

async function getAuthHeaders(headers = {}) {
  const user = getFirebaseAuth()?.currentUser;
  if (!user) {
    throw new Error("Sign in with Firebase to use MongoDB Atlas.");
  }

  return {
    ...headers,
    Authorization: `Bearer ${await user.getIdToken()}`
  };
}

/**
 * Tests connection to MongoDB Atlas
 */
export async function testMongoConnection() {
  try {
    const res = await withTimeout(
      fetch(`${API_BASE}/api/mongodb/test`, {
        method: 'POST',
        headers: await getAuthHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify({})
      }),
      8000
    );

    const data = await res.json().catch(() => ({}));

    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Failed to connect to MongoDB Atlas cluster.');
    }

    return data;
  } catch (err) {
    console.error("MongoDB Atlas test error:", err);
    throw err;
  }
}

/**
 * Fetches student records from MongoDB Atlas
 */
export async function getStudentsFromMongo() {
  try {
    const res = await withTimeout(
      fetch(`${API_BASE}/api/mongodb/students`, {
        method: 'GET',
        headers: await getAuthHeaders({ 'Accept': 'application/json' })
      }),
      4000
    );

    if (!res.ok) return null;
    const data = await res.json();
    if (Array.isArray(data) && data.length > 0) {
      console.log(`🍃 Loaded ${data.length} students from MongoDB Atlas`);
      return data;
    }
    return null;
  } catch (err) {
    // Non-blocking
    return null;
  }
}

/**
 * Saves a single student to MongoDB Atlas (background)
 */
export async function saveStudentToMongo(student, allStudents = null) {
  try {
    const res = await withTimeout(
      fetch(`${API_BASE}/api/mongodb/student`, {
        method: 'POST',
        headers: await getAuthHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify(student)
      }),
      4000
    );

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || `Failed to save to MongoDB (${res.status})`);
    }

    const data = await res.json();
    console.log(`🍃 Synced student ${student.id} to MongoDB Atlas!`);

    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('mongodb-sync-success', {
        detail: { studentId: student.id, action: 'save' }
      }));
    }

    return data;
  } catch (err) {
    console.warn("⚠️ MongoDB Atlas save warning:", err.message);
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('mongodb-sync-error', {
        detail: { message: err.message }
      }));
    }
    return null;
  }
}

/**
 * Deletes a student from MongoDB Atlas (background)
 */
export async function deleteStudentFromMongo(studentId) {
  try {
    const res = await withTimeout(
      fetch(`${API_BASE}/api/mongodb/student?id=${encodeURIComponent(studentId)}`, {
        method: 'DELETE',
        headers: await getAuthHeaders({ 'Accept': 'application/json' })
      }),
      4000
    );

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || `Failed to delete from MongoDB (${res.status})`);
    }

    const data = await res.json();
    console.log(`🍃 Deleted student ${studentId} from MongoDB Atlas!`);

    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('mongodb-sync-success', {
        detail: { studentId, action: 'delete' }
      }));
    }

    return data;
  } catch (err) {
    console.warn("⚠️ MongoDB Atlas delete warning:", err.message);
    return null;
  }
}

/**
 * Bulk syncs all students to MongoDB Atlas
 */
export async function syncAllStudentsToMongo(students) {
  try {
    const res = await withTimeout(
      fetch(`${API_BASE}/api/mongodb/sync`, {
        method: 'POST',
        headers: await getAuthHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify({ students })
      }),
      6000
    );

    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Failed to bulk sync to MongoDB Atlas.');
    }

    console.log(`🍃 Synced all ${students.length} students to MongoDB Atlas!`);
    return data;
  } catch (err) {
    console.warn("⚠️ MongoDB Atlas sync error:", err.message);
    throw err;
  }
}
