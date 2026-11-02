// Firebase Configuration & Credentials
export const firebaseConfig = {
  apiKey: "AIzaSyDfTR0FvNCCclmFwtTHJCmfizXISc-rXDg",
  authDomain: "website-82bc7.firebaseapp.com",
  projectId: "website-82bc7",
  storageBucket: "website-82bc7.firebasestorage.app",
  messagingSenderId: "479303047878",
  appId: "1:479303047878:web:936d5c4331d9a1f75555c7",
  measurementId: "G-LF2PDT3QC0"
};

// Alias for backwards compatibility
export const defaultFirebaseConfig = firebaseConfig;

// Check active Firebase config
export function getActiveFirebaseConfig() {
  // If credentials are provided in this file, use them directly
  if (firebaseConfig && firebaseConfig.apiKey && firebaseConfig.apiKey !== "YOUR_API_KEY" && firebaseConfig.apiKey.length > 10) {
    return firebaseConfig;
  }

  // Otherwise check if user saved a custom config in localStorage
  if (typeof window !== 'undefined' && window.localStorage) {
    const saved = localStorage.getItem('firebase_app_config');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed && parsed.apiKey && parsed.apiKey !== "YOUR_API_KEY") {
          return parsed;
        }
      } catch (e) {
        console.warn("Could not parse saved Firebase config", e);
      }
    }
  }
  return firebaseConfig;
}

export function saveFirebaseConfig(configObj) {
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('firebase_app_config', JSON.stringify(configObj));
  }
}

export function clearFirebaseConfig() {
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.removeItem('firebase_app_config');
  }
}

export function isFirebaseConfigured(config = getActiveFirebaseConfig()) {
  return Boolean(
    config &&
    config.apiKey &&
    config.apiKey !== "YOUR_API_KEY" &&
    config.apiKey.length > 10 &&
    config.projectId &&
    config.projectId !== "YOUR_PROJECT_ID"
  );
}
