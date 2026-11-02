// Dropbox credentials are entered by the user and stored in browser storage.
export const dropboxConfig = {
  accessToken: "",
  appKey: "",
  filePath: "/students.json"
};

const STORAGE_KEY = 'dropbox_app_config';

export function getActiveDropboxConfig() {
  if (typeof window !== 'undefined' && window.localStorage) {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed && parsed.accessToken && parsed.accessToken !== 'YOUR_DROPBOX_ACCESS_TOKEN') {
          return {
            ...dropboxConfig,
            ...parsed
          };
        }
      } catch (e) {
        console.warn("Could not parse saved Dropbox config from localStorage:", e);
      }
    }
  }

  return dropboxConfig;
}

export function saveDropboxConfig(configObj) {
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(configObj));
  }
}

export function clearDropboxConfig() {
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

export function isDropboxConfigured(config = getActiveDropboxConfig()) {
  if (!config) return false;
  const token = config.accessToken;
  return Boolean(
    token &&
    token !== 'YOUR_DROPBOX_ACCESS_TOKEN' &&
    token.trim().length > 15
  );
}
