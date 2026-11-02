// Student Data Store with Instant UI, Resilient Firebase Sync, and Dropbox Cloud Backup
// Saves immediately so UI never hangs, then syncs to Cloud Firestore, Storage & Dropbox
import { 
  saveStudentToDropbox, 
  deleteStudentFromDropbox, 
  getStudentsFromDropbox 
} from './dropbox-service.js';
import { 
  saveStudentToMongo, 
  deleteStudentFromMongo, 
  getStudentsFromMongo 
} from './mongodb-service.js';

const STORAGE_FILE_PATH = 'students.json';
const LOCAL_STORAGE_KEY = 'students_firebase_cache';

const INITIAL_STUDENTS = [
  {
    id: "STU-101",
    name: "Alex Morgan",
    age: 21,
    department: "Computer Science"
  },
  {
    id: "STU-102",
    name: "Sophia Chen",
    age: 20,
    department: "Data Science"
  },
  {
    id: "STU-103",
    name: "Marcus Johnson",
    age: 22,
    department: "Business Administration"
  },
  {
    id: "STU-104",
    name: "Elena Rodriguez",
    age: 19,
    department: "Electrical Engineering"
  },
  {
    id: "STU-105",
    name: "David Kim",
    age: 21,
    department: "Cybersecurity"
  }
];

let firestoreDb = null;
let firestoreModules = null;
let firebaseStorage = null;
let firebaseStorageModules = null;

// Helper to prevent hanging if Firebase database hasn't been created in the console
function withTimeout(promise, ms = 2500) {
  let timeoutId;
  const timeoutPromise = new Promise((_, reject) => {
    timeoutId = setTimeout(() => {
      reject(new Error("Timeout: Firestore/Storage is not enabled in Firebase Console yet."));
    }, ms);
  });
  return Promise.race([
    promise.finally(() => clearTimeout(timeoutId)),
    timeoutPromise
  ]);
}

// Dynamically load Firebase Cloud Firestore
async function getFirestore() {
  const app = getFirebaseApp();
  if (!app) return null;
  if (firestoreDb) return { db: firestoreDb, fs: firestoreModules };

  try {
    const fs = await import("https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js");
    firestoreDb = fs.getFirestore(app);
    firestoreModules = fs;
    return { db: firestoreDb, fs: firestoreModules };
  } catch (err) {
    console.warn("Could not load Firebase Firestore SDK:", err);
    return null;
  }
}

// Dynamically load Firebase Cloud Storage
async function getStorage() {
  const app = getFirebaseApp();
  if (!app) return null;
  if (firebaseStorage) return { storage: firebaseStorage, st: firebaseStorageModules };

  try {
    const st = await import("https://www.gstatic.com/firebasejs/10.12.0/firebase-storage.js");
    firebaseStorage = st.getStorage(app);
    firebaseStorageModules = st;
    return { storage: firebaseStorage, st: firebaseStorageModules };
  } catch (err) {
    console.warn("Could not load Firebase Storage SDK:", err);
    return null;
  }
}

// Local cache helpers
function getLocalCache() {
  try {
    const data = localStorage.getItem(LOCAL_STORAGE_KEY);
    return data ? JSON.parse(data) : null;
  } catch (e) {
    return null;
  }
}

function setLocalCache(students) {
  try {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(students));
  } catch (e) {
    console.warn("Could not save to localStorage cache:", e);
  }
}

// ========================================================
// 1. GET ALL STUDENTS (Fast local return + Cloud background check)
// ========================================================
export async function getStudents() {
  const cached = getLocalCache();

  // Try fetching from Firebase Firestore with strict timeout
  try {
    const fbFs = await getFirestore();
    if (fbFs) {
      const colRef = fbFs.fs.collection(fbFs.db, "students");
      const snapshot = await withTimeout(fbFs.fs.getDocs(colRef), 2000);

      if (!snapshot.empty) {
        const firestoreList = [];
        snapshot.forEach(docSnap => {
          const data = docSnap.data();
          firestoreList.push({
            id: data.id || docSnap.id,
            name: data.name || '',
            age: parseInt(data.age, 10) || 20,
            department: data.department || ''
          });
        });
        setLocalCache(firestoreList);
        return firestoreList;
      }
    }
  } catch (err) {
    console.info("Firestore not initialized or offline. Using local storage:", err.message);
  }

  // Try fetching from Dropbox backup if available
  try {
    const dropboxStudents = await getStudentsFromDropbox();
    if (dropboxStudents && Array.isArray(dropboxStudents) && dropboxStudents.length > 0) {
      setLocalCache(dropboxStudents);
      return dropboxStudents;
    }
  } catch (dbErr) {
    // Non-blocking
  }

  // Try fetching from MongoDB Atlas if available
  try {
    const mongoStudents = await getStudentsFromMongo();
    if (mongoStudents && Array.isArray(mongoStudents) && mongoStudents.length > 0) {
      setLocalCache(mongoStudents);
      return mongoStudents;
    }
  } catch (mongoErr) {
    // Non-blocking
  }

  // Fallback to local cache
  if (cached && Array.isArray(cached) && cached.length > 0) {
    return cached;
  }

  setLocalCache(INITIAL_STUDENTS);
  return [...INITIAL_STUDENTS];
}

// ========================================================
// 2. ADD STUDENT (Instant UI response + Background Cloud Sync)
// ========================================================
export async function addStudent(studentData) {
  const newStudent = {
    id: studentData.id ? studentData.id.trim() : `STU-${Math.floor(100 + Math.random() * 900)}`,
    name: studentData.name.trim(),
    age: parseInt(studentData.age, 10) || 20,
    department: studentData.department.trim()
  };

  // 1. Immediately update local storage so UI is instant
  const current = getLocalCache() || [...INITIAL_STUDENTS];
  current.unshift(newStudent);
  setLocalCache(current);

  // 2. Perform Firebase sync with timeout guard so UI NEVER freezes
  syncStudentToFirebase(newStudent, current);

  // 3. Perform Dropbox cloud backup sync
  saveStudentToDropbox(newStudent, current);

  // 4. Perform MongoDB Atlas cluster sync
  saveStudentToMongo(newStudent, current);

  return newStudent;
}

// Background sync to Firebase
async function syncStudentToFirebase(newStudent, allStudents) {
  let firestoreSuccess = false;

  // A. Save to Cloud Firestore
  try {
    const fbFs = await getFirestore();
    if (fbFs) {
      const docRef = fbFs.fs.doc(fbFs.db, "students", newStudent.id);
      await withTimeout(fbFs.fs.setDoc(docRef, newStudent), 2500);
      firestoreSuccess = true;
      console.log(`✅ Saved ${newStudent.id} to Firebase Firestore!`);
    }
  } catch (fsErr) {
    console.warn("⚠️ Firebase Firestore write:", fsErr.message);
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('firebase-sync-warning', {
        detail: {
          service: 'Firestore',
          message: "Note: To sync online, click 'Create Database' in Firebase Console -> Build -> Firestore Database."
        }
      }));
    }
  }

  // B. Sync to Cloud Storage
  try {
    const fbSt = await getStorage();
    if (fbSt) {
      const storageRef = fbSt.st.ref(fbSt.storage, STORAGE_FILE_PATH);
      const blob = new Blob([JSON.stringify(allStudents, null, 2)], { type: 'application/json' });
      await withTimeout(fbSt.st.uploadBytes(storageRef, blob), 2500);
      console.log(`✅ Synced students to Firebase Storage!`);
    }
  } catch (stErr) {
    // Non-blocking warning
  }
}

// ========================================================
// 3. DELETE STUDENT (Instant UI response + Background Cloud Sync)
// ========================================================
export async function deleteStudent(studentId) {
  const current = getLocalCache() || [...INITIAL_STUDENTS];
  const updated = current.filter(s => s.id !== studentId);
  setLocalCache(updated);

  // 1. Background delete from Firebase
  syncDeleteFromFirebase(studentId, updated);

  // 2. Background sync updated list to Dropbox
  deleteStudentFromDropbox(studentId, updated);

  // 3. Background delete from MongoDB Atlas
  deleteStudentFromMongo(studentId);

  return updated;
}

async function syncDeleteFromFirebase(studentId, allStudents) {
  try {
    const fbFs = await getFirestore();
    if (fbFs) {
      const docRef = fbFs.fs.doc(fbFs.db, "students", studentId);
      await withTimeout(fbFs.fs.deleteDoc(docRef), 2500);
      console.log(`✅ Deleted ${studentId} from Firebase Firestore!`);
    }
  } catch (fsErr) {
    console.warn("Firebase Firestore delete:", fsErr.message);
  }

  try {
    const fbSt = await getStorage();
    if (fbSt) {
      const storageRef = fbSt.st.ref(fbSt.storage, STORAGE_FILE_PATH);
      const blob = new Blob([JSON.stringify(allStudents, null, 2)], { type: 'application/json' });
      await withTimeout(fbSt.st.uploadBytes(storageRef, blob), 2500);
    }
  } catch (stErr) {
    // Non-blocking
  }
}

// Get student by ID
export function getStudentById(studentId) {
  const cached = getLocalCache() || INITIAL_STUDENTS;
  return cached.find(s => s.id === studentId) || null;
}
