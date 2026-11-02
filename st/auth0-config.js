// Auth0 Configuration & Credentials Management
// Store your Auth0 Application credentials here or configure them via the Settings modal in the app.

export const auth0Config = {
  // Replace with your Auth0 Domain from the Auth0 Dashboard (e.g. "dev-xyz.us.auth0.com")
  domain: "dev-58o1wuwbx3qv1hfn.us.auth0.com",

  // Replace with your Auth0 Client ID from your Single Page Application settings
  clientId: "gfVRUJImJBzE3d1wagWVlM2DNMwQD6iS",

  // Optional audience for custom API authorization
  audience: "",

  // Standard OIDC scopes for user identity & email profile
  scope: "openid profile email"
};

// Key used in browser localStorage to persist runtime settings
const STORAGE_KEY = 'auth0_app_config';

/**
 * Returns the currently active Auth0 configuration:
 * Prioritizes custom settings saved by the user in the UI, then falls back to defaults above.
 */
export function getActiveAuth0Config() {
  // If real credentials are provided in this file, prioritize them directly
  if (auth0Config && 
      auth0Config.domain && 
      auth0Config.domain !== 'YOUR_AUTH0_DOMAIN' && 
      auth0Config.domain !== 'dev-sample.us.auth0.com' &&
      auth0Config.clientId && 
      auth0Config.clientId !== 'YOUR_AUTH0_CLIENT_ID') {
    return auth0Config;
  }

  if (typeof window !== 'undefined' && window.localStorage) {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed && parsed.domain && parsed.clientId) {
          return {
            ...auth0Config,
            ...parsed
          };
        }
      } catch (e) {
        console.warn("Could not parse saved Auth0 config from localStorage:", e);
      }
    }
  }
  return auth0Config;
}

/**
 * Persists updated Auth0 credentials to localStorage
 */
export function saveAuth0Config(configObj) {
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(configObj));
  }
}

/**
 * Resets Auth0 credentials in localStorage
 */
export function clearAuth0Config() {
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

/**
 * Validates whether real Auth0 credentials have been provided
 */
export function isAuth0Configured(config = getActiveAuth0Config()) {
  if (!config) return false;
  const { domain, clientId } = config;
  const isPlaceholderDomain = !domain ||
    domain === 'YOUR_AUTH0_DOMAIN' ||
    domain === 'YOUR_AUTH0_DOMAIN.auth0.com' ||
    domain === 'dev-sample.us.auth0.com';
  const isPlaceholderClient = !clientId ||
    clientId === 'YOUR_AUTH0_CLIENT_ID' ||
    clientId.length < 6;

  return Boolean(!isPlaceholderDomain && !isPlaceholderClient && domain.includes('.'));
}
