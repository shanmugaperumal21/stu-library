import { getActiveFirebaseConfig, isFirebaseConfigured } from './firebase-config.js';

let firebaseApp = null;
let firebaseAuth = null;
let isRealFirebase = false;

// Dynamic import helpers for Firebase modular SDK
let fbModules = null;

// Format Firebase Auth errors into clear, friendly guidance
export function formatFirebaseError(error) {
  if (!error) return "An unknown error occurred.";
  const code = error.code || '';
  switch (code) {
    case 'auth/invalid-credential':
    case 'auth/user-not-found':
    case 'auth/wrong-password':
      return "Incorrect email or password. If you haven't registered yet, please switch to the 'Register' tab first.";
    case 'auth/email-already-in-use':
      return "An account with this email already exists. Please switch to the 'Sign In' tab.";
    case 'auth/weak-password':
      return "Password is too weak. Please use at least 6 characters.";
    case 'auth/invalid-email':
      return "Please enter a valid email address.";
    case 'auth/operation-not-allowed':
      return "⚠️ Email/Password provider is not enabled in Firebase! Go to Firebase Console -> Build -> Authentication -> Sign-in method -> Enable 'Email/Password'.";
    case 'auth/network-request-failed':
      return "Network connection error. Please check your internet connection.";
    case 'auth/popup-closed-by-user':
      return "Google Sign-In popup was closed before completing.";
    case 'auth/unauthorized-domain':
      return "Domain unauthorized. Add 'localhost' in Firebase Console -> Authentication -> Settings -> Authorized domains.";
    default:
      return error.message || "An authentication error occurred.";
  }
}

async function loadFirebaseModules() {
  if (fbModules) return fbModules;
  try {
    const [appMod, authMod] = await Promise.all([
      import("https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js"),
      import("https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js")
    ]);
    fbModules = {
      initializeApp: appMod.initializeApp,
      getApps: appMod.getApps,
      getApp: appMod.getApp,
      getAuth: authMod.getAuth,
      signInWithEmailAndPassword: authMod.signInWithEmailAndPassword,
      createUserWithEmailAndPassword: authMod.createUserWithEmailAndPassword,
      signOut: authMod.signOut,
      onAuthStateChanged: authMod.onAuthStateChanged,
      GoogleAuthProvider: authMod.GoogleAuthProvider,
      signInWithPopup: authMod.signInWithPopup,
      updateProfile: authMod.updateProfile
    };
    return fbModules;
  } catch (err) {
    console.warn("Could not load Firebase CDN modules, falling back to local simulation:", err);
    return null;
  }
}

export function getFirebaseApp() {
  return firebaseApp;
}

export function getFirebaseAuth() {
  return firebaseAuth;
}

export async function initializeAuthSystem(onStateChangeCallback) {
  const config = getActiveFirebaseConfig();
  
  if (isFirebaseConfigured(config)) {
    try {
      const fb = await loadFirebaseModules();
      if (fb) {
        // Prevent duplicate app initialization
        const existingApps = fb.getApps();
        firebaseApp = existingApps.length > 0 ? fb.getApp() : fb.initializeApp(config);
        firebaseAuth = fb.getAuth(firebaseApp);
        isRealFirebase = true;

        fb.onAuthStateChanged(firebaseAuth, (user) => {
          if (user) {
            onStateChangeCallback({
              uid: user.uid,
              email: user.email,
              displayName: user.displayName || user.email.split('@')[0],
              photoURL: user.photoURL || null,
              isRealFirebase: true
            });
          } else {
            onStateChangeCallback(null);
          }
        });

        return { success: true, mode: 'firebase' };
      }
    } catch (err) {
      console.error("Firebase initialization failed:", err);
      // Fallback to local
    }
  }

  // Local demo simulation mode
  isRealFirebase = false;
  const currentUser = getLocalCurrentUser();
  onStateChangeCallback(currentUser);
  return { success: true, mode: 'local' };
}

// Check current mode
export function getAuthMode() {
  return isRealFirebase ? 'firebase' : 'local';
}

// Local mock storage helpers
function getLocalUsers() {
  try {
    return JSON.parse(localStorage.getItem('student_app_mock_users') || '[]');
  } catch {
    return [];
  }
}

function saveLocalUsers(users) {
  localStorage.setItem('student_app_mock_users', JSON.stringify(users));
}

function getLocalCurrentUser() {
  try {
    const user = JSON.parse(localStorage.getItem('student_app_current_user'));
    return user ? { ...user, isRealFirebase: false } : null;
  } catch {
    return null;
  }
}

function setLocalCurrentUser(user) {
  if (user) {
    localStorage.setItem('student_app_current_user', JSON.stringify(user));
  } else {
    localStorage.removeItem('student_app_current_user');
  }
}

// Login
export async function loginUser(email, password) {
  if (isRealFirebase && firebaseAuth) {
    const fb = await loadFirebaseModules();
    try {
      const cred = await fb.signInWithEmailAndPassword(firebaseAuth, email, password);
      return {
        uid: cred.user.uid,
        email: cred.user.email,
        displayName: cred.user.displayName || cred.user.email.split('@')[0],
        photoURL: cred.user.photoURL || null,
        isRealFirebase: true
      };
    } catch (err) {
      throw new Error(formatFirebaseError(err));
    }
  } else {
    // Local mode verification
    const users = getLocalUsers();
    const user = users.find(u => u.email.toLowerCase() === email.toLowerCase());
    if (!user) {
      throw new Error("No account found with this email. Please click 'Register' tab to create an account first.");
    }
    if (user.password !== password) {
      throw new Error("Incorrect password. Please try again.");
    }
    const sessionUser = {
      uid: user.uid,
      email: user.email,
      displayName: user.name || user.email.split('@')[0],
      photoURL: null,
      isRealFirebase: false
    };
    setLocalCurrentUser(sessionUser);
    return sessionUser;
  }
}

// Register
export async function registerUser(name, email, password) {
  if (isRealFirebase && firebaseAuth) {
    const fb = await loadFirebaseModules();
    try {
      const cred = await fb.createUserWithEmailAndPassword(firebaseAuth, email, password);
      if (name && fb.updateProfile) {
        try {
          await fb.updateProfile(cred.user, { displayName: name });
        } catch (e) {
          console.warn("Could not update display name:", e);
        }
      }
      return {
        uid: cred.user.uid,
        email: cred.user.email,
        displayName: name || cred.user.email.split('@')[0],
        photoURL: null,
        isRealFirebase: true
      };
    } catch (err) {
      throw new Error(formatFirebaseError(err));
    }
  } else {
    // Local mode registration
    const users = getLocalUsers();
    if (users.some(u => u.email.toLowerCase() === email.toLowerCase())) {
      throw new Error("An account with this email already exists. Please log in.");
    }
    const newUser = {
      uid: 'user_' + Date.now(),
      name: name.trim(),
      email: email.trim().toLowerCase(),
      password: password
    };
    users.push(newUser);
    saveLocalUsers(users);

    const sessionUser = {
      uid: newUser.uid,
      email: newUser.email,
      displayName: newUser.name || newUser.email.split('@')[0],
      photoURL: null,
      isRealFirebase: false
    };
    setLocalCurrentUser(sessionUser);
    return sessionUser;
  }
}

// Google Sign-In
export async function loginWithGoogle() {
  if (isRealFirebase && firebaseAuth) {
    const fb = await loadFirebaseModules();
    try {
      const provider = new fb.GoogleAuthProvider();
      const cred = await fb.signInWithPopup(firebaseAuth, provider);
      return {
        uid: cred.user.uid,
        email: cred.user.email,
        displayName: cred.user.displayName || cred.user.email.split('@')[0],
        photoURL: cred.user.photoURL || null,
        isRealFirebase: true
      };
    } catch (err) {
      throw new Error(formatFirebaseError(err));
    }
  } else {
    // Simulated Google Login for demo
    const mockGoogleUser = {
      uid: 'google_user_' + Date.now(),
      email: 'demo.student@gmail.com',
      displayName: 'Demo Student',
      photoURL: null,
      isRealFirebase: false
    };
    setLocalCurrentUser(mockGoogleUser);
    return mockGoogleUser;
  }
}

// Logout
export async function logoutUser() {
  if (isRealFirebase && firebaseAuth) {
    const fb = await loadFirebaseModules();
    await fb.signOut(firebaseAuth);
  } else {
    setLocalCurrentUser(null);
  }
}
