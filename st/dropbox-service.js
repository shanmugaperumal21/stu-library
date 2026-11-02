// Dropbox Storage Service
// Handles file upload, download, and student synchronization using Dropbox Files API v2.
import { getActiveDropboxConfig, isDropboxConfigured } from './dropbox-config.js';

const DROPBOX_UPLOAD_URL = 'https://content.dropboxapi.com/2/files/upload';
const DROPBOX_DOWNLOAD_URL = 'https://content.dropboxapi.com/2/files/download';
const DROPBOX_ACCOUNT_URL = 'https://api.dropboxapi.com/2/users/get_current_account';

/**
 * Timeout helper to avoid UI hanging if network is slow or offline
 */
function withTimeout(promise, ms = 4000) {
  let timeoutId;
  const timeoutPromise = new Promise((_, reject) => {
    timeoutId = setTimeout(() => {
      reject(new Error("Timeout connecting to Dropbox API"));
    }, ms);
  });
  return Promise.race([
    promise.finally(() => clearTimeout(timeoutId)),
    timeoutPromise
  ]);
}

/**
 * Formats Dropbox error messages into clean, readable text
 */
export function formatDropboxError(error) {
  if (!error) return "An unknown error occurred connecting to Dropbox.";
  const msg = error.message || String(error);
  if (msg.includes('missing_scope') || msg.includes('files.content.write') || msg.includes('files.content.read')) {
    return "Dropbox token is missing file permissions! In Dropbox App Console > Permissions tab, enable 'files.content.write' and 'files.content.read', click Submit, then click Generate to create a new token.";
  }
  if (msg.includes('invalid_access_token') || msg.includes('401')) {
    return "Invalid or expired Dropbox Access Token. Please update your token in Settings.";
  }
  if (msg.includes('path/not_found') || msg.includes('409')) {
    return "The requested file (/students.json) was not found in your Dropbox folder yet.";
  }
  if (msg.includes('Failed to fetch') || msg.includes('Network')) {
    return "Network error connecting to Dropbox. Please check your internet connection.";
  }
  return msg;
}

/**
 * Tests connection to Dropbox using the active access token
 */
export async function testDropboxConnection() {
  const config = getActiveDropboxConfig();
  if (!isDropboxConfigured(config)) {
    throw new Error("Dropbox is not configured yet. Please provide an Access Token.");
  }

  try {
    const res = await withTimeout(
      fetch(DROPBOX_ACCOUNT_URL, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${config.accessToken.trim()}`
        }
      }),
      4000
    );

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      const summary = errData.error_summary || res.statusText;
      throw new Error(`Dropbox authentication failed: ${summary}`);
    }

    const account = await res.json();
    const accountName = (account.name && account.name.display_name) || account.email || 'Dropbox User';

    // Verify if file permissions (files.content.write / files.metadata.read) are enabled
    try {
      const scopeCheck = await fetch('https://api.dropboxapi.com/2/files/list_folder', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${config.accessToken.trim()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ path: '' })
      });
      if (!scopeCheck.ok) {
        const scopeData = await scopeCheck.json().catch(() => ({}));
        if (scopeData.error && scopeData.error['.tag'] === 'missing_scope') {
          throw new Error(`Account connected (${accountName}), but token is missing file permissions! In Dropbox App Console > Permissions tab, enable 'files.content.write' and 'files.content.read', click Submit, then click Generate to create a new token.`);
        }
      }
    } catch (scopeErr) {
      if (scopeErr.message.includes('missing file permissions')) {
        throw scopeErr;
      }
    }

    return {
      success: true,
      email: account.email,
      name: accountName
    };
  } catch (err) {
    console.error("Dropbox connection test failed:", err);
    throw new Error(formatDropboxError(err));
  }
}

/**
 * Uploads student records JSON to Dropbox
 */
export async function uploadStudentsToDropbox(students) {
  const config = getActiveDropboxConfig();
  if (!isDropboxConfigured(config)) {
    return null;
  }

  const filePath = (config.filePath || '/students.json').trim();
  const fileContent = JSON.stringify(students, null, 2);

  try {
    const res = await withTimeout(
      fetch(DROPBOX_UPLOAD_URL, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${config.accessToken.trim()}`,
          'Dropbox-API-Arg': JSON.stringify({
            path: filePath,
            mode: 'overwrite',
            autorename: false,
            mute: true,
            strict_conflict: false
          }),
          'Content-Type': 'application/octet-stream'
        },
        body: fileContent
      }),
      5000
    );

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error_summary || `Dropbox upload failed (${res.status})`);
    }

    const data = await res.json();
    console.log(`✅ Synced ${students.length} students to Dropbox (${filePath})!`);

    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('dropbox-sync-success', {
        detail: { count: students.length, path: filePath }
      }));
    }

    return data;
  } catch (err) {
    console.warn("⚠️ Dropbox background sync warning:", err.message);
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('dropbox-sync-error', {
        detail: { message: formatDropboxError(err) }
      }));
    }
    return null;
  }
}

/**
 * Downloads student records from Dropbox if file exists
 */
export async function getStudentsFromDropbox() {
  const config = getActiveDropboxConfig();
  if (!isDropboxConfigured(config)) {
    return null;
  }

  const filePath = (config.filePath || '/students.json').trim();

  try {
    const res = await withTimeout(
      fetch(DROPBOX_DOWNLOAD_URL, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${config.accessToken.trim()}`,
          'Dropbox-API-Arg': JSON.stringify({
            path: filePath
          })
        }
      }),
      4000
    );

    if (!res.ok) {
      // If file doesn't exist yet, return null cleanly
      return null;
    }

    const data = await res.json();
    if (Array.isArray(data) && data.length > 0) {
      console.log(`✅ Loaded ${data.length} students from Dropbox (${filePath})`);
      return data;
    }
    return null;
  } catch (err) {
    console.info("Dropbox download info:", err.message);
    return null;
  }
}

/**
 * Convenience helper to save student to Dropbox in background
 */
export async function saveStudentToDropbox(newStudent, allStudents) {
  return uploadStudentsToDropbox(allStudents);
}

/**
 * Convenience helper to delete student from Dropbox in background
 */
export async function deleteStudentFromDropbox(studentId, allStudents) {
  return uploadStudentsToDropbox(allStudents);
}
