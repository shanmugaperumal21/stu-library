// Auth0 Authentication Service
// Dedicated module for Auth0 SPA SDK integration, token handling, and session state.
import { getActiveAuth0Config, isAuth0Configured } from './auth0-config.js';

let auth0ClientInstance = null;
let auth0SdkModule = null;

const DEMO_USER_STORAGE_KEY = 'student_app_auth0_demo_user';

/**
 * Friendly error messages for common Auth0 configuration / authentication issues
 */
export function formatAuth0Error(error) {
  if (!error) return "An unknown error occurred during Auth0 authentication.";
  const msg = error.message || error.error_description || String(error);

  if (msg.includes('Callback URL mismatch') || msg.includes('redirect_uri')) {
    return "⚠️ Auth0 Callback URL mismatch! Please open your Auth0 Dashboard -> Applications -> Your App -> Add 'http://localhost:3000' to 'Allowed Callback URLs', 'Allowed Logout URLs', and 'Allowed Web Origins'.";
  }
  if (msg.includes('Popup was closed') || msg.includes('popup_closed')) {
    return "Auth0 login window was closed before completing.";
  }
  if (msg.includes('Unauthorized') || msg.includes('client not found')) {
    return "Invalid Auth0 Client ID or Domain. Please verify your credentials in Settings.";
  }
  if (msg.includes('access_denied') || msg.includes('user cancelled')) {
    return "Authentication was cancelled by the user.";
  }
  if (msg.includes('Network') || msg.includes('Failed to fetch')) {
    return "Network error connecting to Auth0. Please verify your internet connection and Auth0 domain.";
  }

  return msg;
}

/**
 * Dynamically loads the Auth0 SPA SDK either from window.auth0 (CDN)
 * or via dynamic ES module import from CDN as fallback.
 */
async function loadAuth0Sdk() {
  if (typeof window !== 'undefined' && window.auth0 && window.auth0.createAuth0Client) {
    return window.auth0.createAuth0Client;
  }

  if (auth0SdkModule) {
    return auth0SdkModule;
  }

  try {
    const mod = await import("https://cdn.jsdelivr.net/npm/@auth0/auth0-spa-js@2.1.3/+esm");
    if (mod && mod.createAuth0Client) {
      auth0SdkModule = mod.createAuth0Client;
      return auth0SdkModule;
    }
  } catch (err) {
    console.warn("Could not import Auth0 ESM module, checking window.auth0:", err);
  }

  if (typeof window !== 'undefined' && window.auth0 && window.auth0.createAuth0Client) {
    return window.auth0.createAuth0Client;
  }

  return null;
}

/**
 * Instantiates or retrieves the cached Auth0Client instance
 */
export async function getAuth0Client() {
  if (auth0ClientInstance) return auth0ClientInstance;

  const config = getActiveAuth0Config();
  if (!isAuth0Configured(config)) {
    return null;
  }

  try {
    const createClient = await loadAuth0Sdk();
    if (!createClient) {
      console.warn("Auth0 SPA SDK is not loaded.");
      return null;
    }

    const redirectUri = window.location.origin + window.location.pathname;

    auth0ClientInstance = await createClient({
      domain: config.domain.trim(),
      clientId: config.clientId.trim(),
      authorizationParams: {
        redirect_uri: redirectUri,
        scope: config.scope || 'openid profile email',
        ...(config.audience ? { audience: config.audience } : {})
      },
      cacheLocation: 'localstorage',
      useRefreshTokens: true
    });

    return auth0ClientInstance;
  } catch (err) {
    console.error("Failed to initialize Auth0 client:", err);
    throw err;
  }
}

/**
 * Normalizes Auth0 user object to match application's standard user schema
 */
export function normalizeAuth0User(rawUser) {
  if (!rawUser) return null;

  const displayName = rawUser.name || 
    rawUser.nickname || 
    (rawUser.email ? rawUser.email.split('@')[0] : 'Auth0 User');

  return {
    uid: rawUser.sub || `auth0_${Date.now()}`,
    email: rawUser.email || `${rawUser.nickname || 'user'}@auth0.user`,
    displayName: displayName,
    photoURL: rawUser.picture || null,
    provider: 'auth0',
    isAuth0: true,
    raw: rawUser
  };
}

/**
 * Checks if the browser currently has an incoming Auth0 redirect callback (code & state in query params)
 * and exchanges the code for tokens.
 */
export async function checkAuth0RedirectCallback() {
  if (typeof window === 'undefined') return null;

  const query = window.location.search;
  const isRedirect = query.includes('code=') && query.includes('state=');

  if (!isRedirect) return null;

  try {
    const client = await getAuth0Client();
    if (client) {
      await client.handleRedirectCallback();
      // Remove query parameters from address bar cleanly
      window.history.replaceState({}, document.title, window.location.pathname);
      const rawUser = await client.getUser();
      return normalizeAuth0User(rawUser);
    }
  } catch (err) {
    console.error("Auth0 redirect callback processing failed:", err);
    window.history.replaceState({}, document.title, window.location.pathname);
    throw new Error(formatAuth0Error(err));
  }

  return null;
}

/**
 * Checks if an active Auth0 session exists (persisted in cache/localStorage or demo)
 */
export async function checkAuth0Session() {
  // 1. Check if demo session is stored
  const demo = getAuth0DemoUser();
  if (demo) return demo;

  // 2. Check if real Auth0 credentials configured
  if (!isAuth0Configured()) return null;

  try {
    const client = await getAuth0Client();
    if (!client) return null;

    const isAuthed = await client.isAuthenticated();
    if (isAuthed) {
      const rawUser = await client.getUser();
      return normalizeAuth0User(rawUser);
    }
  } catch (err) {
    console.warn("Auth0 session check warning:", err.message);
  }

  return null;
}

/**
 * Login with Google through Auth0
 * Directs authentication to Google OAuth via Auth0 connection
 */
export async function loginWithAuth0Google() {
  const config = getActiveAuth0Config();

  // If credentials are not yet configured, provide demo session
  if (!isAuth0Configured(config)) {
    return loginWithAuth0Demo('Google Student', 'student@gmail.com');
  }

  try {
    const client = await getAuth0Client();
    if (!client) {
      throw new Error("Unable to initialize authentication client.");
    }

    // Attempt popup with direct Google connection
    try {
      await client.loginWithPopup({
        authorizationParams: {
          connection: 'google-oauth2'
        }
      });
      const rawUser = await client.getUser();
      return normalizeAuth0User(rawUser);
    } catch (popupErr) {
      console.warn("Direct google-oauth2 popup attempt, trying universal login popup:", popupErr);
      // Fallback: standard popup if specific connection name differs
      await client.loginWithPopup();
      const rawUser = await client.getUser();
      return normalizeAuth0User(rawUser);
    }
  } catch (err) {
    console.error("Google authentication error:", err);
    const msg = err.message || '';
    // If popup was blocked by browser, fallback to redirect
    if (msg.includes('popup') || msg.includes('Popup')) {
      try {
        const client = await getAuth0Client();
        const redirectUri = window.location.origin + window.location.pathname;
        await client.loginWithRedirect({
          authorizationParams: {
            connection: 'google-oauth2',
            redirect_uri: redirectUri
          }
        });
        return null;
      } catch (redirectErr) {
        throw new Error(formatAuth0Error(redirectErr));
      }
    }
    throw new Error(formatAuth0Error(err));
  }
}

/**
 * Login using Auth0 Popup (recommended for seamless in-app authentication)
 */
export async function loginWithAuth0Popup() {
  const config = getActiveAuth0Config();

  // If Auth0 credentials not yet configured by user, provide simulated login option
  if (!isAuth0Configured(config)) {
    return loginWithAuth0Demo();
  }

  try {
    const client = await getAuth0Client();
    if (!client) {
      throw new Error("Unable to create Auth0 Client. Please check your internet connection.");
    }

    await client.loginWithPopup();
    const rawUser = await client.getUser();
    return normalizeAuth0User(rawUser);
  } catch (err) {
    console.error("Auth0 popup login error:", err);
    throw new Error(formatAuth0Error(err));
  }
}

/**
 * Login using Auth0 Universal Login Redirect
 */
export async function loginWithAuth0Redirect() {
  const config = getActiveAuth0Config();

  if (!isAuth0Configured(config)) {
    return loginWithAuth0Demo();
  }

  try {
    const client = await getAuth0Client();
    if (!client) {
      throw new Error("Unable to initialize Auth0 client for redirect.");
    }

    const redirectUri = window.location.origin + window.location.pathname;
    await client.loginWithRedirect({
      authorizationParams: {
        redirect_uri: redirectUri
      }
    });
  } catch (err) {
    console.error("Auth0 redirect login error:", err);
    throw new Error(formatAuth0Error(err));
  }
}

/**
 * Simulated Auth0 login for instant local testing when tenant credentials are not yet set
 */
export function loginWithAuth0Demo(customName = 'Auth0 Demo User', customEmail = 'auth0.student@example.com') {
  const demoUser = {
    uid: 'auth0|demo_' + Date.now(),
    email: customEmail,
    displayName: customName,
    photoURL: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&h=120&q=80',
    provider: 'auth0',
    isAuth0: true,
    isDemo: true
  };

  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem(DEMO_USER_STORAGE_KEY, JSON.stringify(demoUser));
  }
  return demoUser;
}

function getAuth0DemoUser() {
  if (typeof window !== 'undefined' && window.localStorage) {
    const item = localStorage.getItem(DEMO_USER_STORAGE_KEY);
    if (item) {
      try {
        return JSON.parse(item);
      } catch (e) {
        return null;
      }
    }
  }
  return null;
}

/**
 * Sign out of Auth0 session
 */
export async function logoutAuth0() {
  // Clear any demo user
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.removeItem(DEMO_USER_STORAGE_KEY);
  }

  if (isAuth0Configured()) {
    try {
      const client = await getAuth0Client();
      if (client && await client.isAuthenticated()) {
        const returnUri = window.location.origin + window.location.pathname;
        await client.logout({
          logoutParams: {
            returnTo: returnUri
          }
        });
      }
    } catch (err) {
      console.warn("Auth0 SDK logout warning:", err.message);
    }
  }

  // Clear client cache instance
  auth0ClientInstance = null;
}
