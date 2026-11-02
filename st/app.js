import { 
  initializeAuthSystem, 
  loginUser, 
  registerUser, 
  loginWithGoogle, 
  logoutUser,
  getAuthMode
} from './auth-service.js';

import { 
  getActiveFirebaseConfig, 
  saveFirebaseConfig, 
  clearFirebaseConfig, 
  isFirebaseConfigured 
} from './firebase-config.js';

import { 
  checkAuth0RedirectCallback, 
  checkAuth0Session, 
  loginWithAuth0Google, 
  loginWithAuth0Demo, 
  logoutAuth0 
} from './auth0-service.js';

import { 
  getActiveAuth0Config, 
  saveAuth0Config, 
  clearAuth0Config, 
  isAuth0Configured 
} from './auth0-config.js';

import { 
  getStudents, 
  addStudent, 
  deleteStudent, 
  getStudentById 
} from './student-data.js';

import { 
  getActiveDropboxConfig, 
  saveDropboxConfig, 
  clearDropboxConfig, 
  isDropboxConfigured 
} from './dropbox-config.js';

import { 
  testDropboxConnection 
} from './dropbox-service.js';

import { 
  getActiveMongoConfig
} from './mongodb-config.js';

import { 
  testMongoConnection, 
  syncAllStudentsToMongo 
} from './mongodb-service.js';

// Application State
let currentUser = null;
let currentStudents = [];
let pendingDeleteStudentId = null;

// DOM Elements
const authView = document.getElementById('auth-view');
const dashboardView = document.getElementById('dashboard-view');

const tabLoginBtn = document.getElementById('tab-login-btn');
const tabRegisterBtn = document.getElementById('tab-register-btn');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const authSubtitle = document.getElementById('auth-subtitle');
const btnLoginSubmit = document.getElementById('btn-login-submit');
const btnRegisterSubmit = document.getElementById('btn-register-submit');
const btnGoogleAuth = document.getElementById('btn-google-auth');
const btnAuth0Auth = document.getElementById('btn-auth0-auth');

const userAvatar = document.getElementById('user-avatar');
const userEmailDisplay = document.getElementById('user-email-display');
const btnLogout = document.getElementById('btn-logout');
const firebaseStatusPill = document.getElementById('firebase-status-pill');
const firebaseStatusLabel = document.getElementById('firebase-status-label');
const authStatusText = document.getElementById('auth-status-text');
const hintTagFirebase = document.getElementById('hint-tag-firebase');
const hintTagAuth0 = document.getElementById('hint-tag-auth0');

const statTotalStudents = document.getElementById('stat-total-students');
const statAvgAge = document.getElementById('stat-avg-age');
const statCoursesCount = document.getElementById('stat-courses-count');

const searchInput = document.getElementById('search-input');
const courseFilter = document.getElementById('course-filter');
const statusFilter = document.getElementById('status-filter');
const studentTableBody = document.getElementById('student-table-body');
const emptyStateView = document.getElementById('empty-state-view');
const tableResultsCounter = document.getElementById('table-results-counter');

const btnOpenAddStudent = document.getElementById('btn-open-add-student');
const btnEmptyAddStudent = document.getElementById('btn-empty-add-student');
const addStudentForm = document.getElementById('add-student-form');

const modalAddStudent = document.getElementById('modal-add-student');
const modalViewStudent = document.getElementById('modal-view-student');
const modalDeleteStudent = document.getElementById('modal-delete-student');
const modalFirebaseConfig = document.getElementById('modal-firebase-config');

const btnConfirmDelete = document.getElementById('btn-confirm-delete');
const deleteStudentName = document.getElementById('delete-student-name');

// Settings Modal DOM Elements (Firebase & Auth0)
const btnOpenFirebaseConfig = document.getElementById('btn-open-firebase-config');
const btnNavFirebaseConfig = document.getElementById('btn-nav-firebase-config');
const tabCfgFirebase = document.getElementById('tab-cfg-firebase');
const tabCfgAuth0 = document.getElementById('tab-cfg-auth0');
const panelCfgFirebase = document.getElementById('panel-cfg-firebase');
const panelCfgAuth0 = document.getElementById('panel-cfg-auth0');

const btnSaveFirebaseConfig = document.getElementById('btn-save-firebase-config');
const btnResetFirebaseConfig = document.getElementById('btn-reset-firebase-config');
const cfgApiKey = document.getElementById('cfg-api-key');
const cfgAuthDomain = document.getElementById('cfg-auth-domain');
const cfgProjectId = document.getElementById('cfg-project-id');
const cfgAppId = document.getElementById('cfg-app-id');

const btnSaveAuth0Config = document.getElementById('btn-save-auth0-config');
const btnResetAuth0Config = document.getElementById('btn-reset-auth0-config');
const btnDemoAuth0Trigger = document.getElementById('btn-demo-auth0-trigger');
const cfgAuth0Domain = document.getElementById('cfg-auth0-domain');
const cfgAuth0ClientId = document.getElementById('cfg-auth0-client-id');

const tabCfgDropbox = document.getElementById('tab-cfg-dropbox');
const panelCfgDropbox = document.getElementById('panel-cfg-dropbox');
const cfgDropboxToken = document.getElementById('cfg-dropbox-token');
const cfgDropboxPath = document.getElementById('cfg-dropbox-path');
const btnSaveDropboxConfig = document.getElementById('btn-save-dropbox-config');
const btnResetDropboxConfig = document.getElementById('btn-reset-dropbox-config');
const btnTestDropboxConfig = document.getElementById('btn-test-dropbox-config');

const tabCfgMongo = document.getElementById('tab-cfg-mongo');
const panelCfgMongo = document.getElementById('panel-cfg-mongo');
const cfgMongoDbName = document.getElementById('cfg-mongo-dbname');
const cfgMongoCollection = document.getElementById('cfg-mongo-collection');
const btnTestMongoConfig = document.getElementById('btn-test-mongo-config');
const btnSyncMongoNow = document.getElementById('btn-sync-mongo-now');

// ========================================================
// TOAST NOTIFICATION UTILITY
// ========================================================
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  const iconSvg = type === 'success' 
    ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`
    : type === 'error'
    ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`
    : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4f46e5" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`;

  toast.innerHTML = `${iconSvg} <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(30px)';
    setTimeout(() => toast.remove(), 250);
  }, 4000);
}

// ========================================================
// MODAL MANAGEMENT
// ========================================================
function openModal(modalEl) {
  if (modalEl) modalEl.classList.add('active');
}

function closeModal(modalEl) {
  if (modalEl) modalEl.classList.remove('active');
}

document.querySelectorAll('[data-close]').forEach(btn => {
  btn.addEventListener('click', (e) => {
    const modalId = e.currentTarget.getAttribute('data-close');
    closeModal(document.getElementById(modalId));
  });
});

// Close modal when clicking on overlay outside modal-container
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeModal(overlay);
  });
});

// ========================================================
// AUTH VIEW TABS & SWITCHING
// ========================================================
tabLoginBtn.addEventListener('click', () => {
  tabLoginBtn.classList.add('active');
  tabRegisterBtn.classList.remove('active');
  loginForm.style.display = 'block';
  registerForm.style.display = 'none';
  authSubtitle.textContent = 'Sign in to manage student records';
});

tabRegisterBtn.addEventListener('click', () => {
  tabRegisterBtn.classList.add('active');
  tabLoginBtn.classList.remove('active');
  loginForm.style.display = 'none';
  registerForm.style.display = 'block';
  authSubtitle.textContent = 'Create your administrator account';
});

// ========================================================
// AUTH STATUS INDICATOR
// ========================================================
function updateAuthStatusBadge() {
  if (currentUser) {
    firebaseStatusPill.className = 'status-badge active';
    firebaseStatusLabel.textContent = 'Active Session';
  } else {
    firebaseStatusPill.className = 'status-badge';
    firebaseStatusLabel.textContent = 'Ready';
  }
}

// ========================================================
// ROUTING & AUTH STATE CHANGE
// ========================================================
async function handleAuthStateChanged(user) {
  currentUser = user;
  updateAuthStatusBadge();

  if (user) {
    // Show Dashboard
    authView.classList.add('hidden');
    dashboardView.classList.remove('hidden');

    const displayName = user.displayName || user.email.split('@')[0];
    userEmailDisplay.textContent = user.email;

    // Set avatar: profile photo if present, otherwise initial
    if (user.photoURL) {
      userAvatar.innerHTML = `<img src="${user.photoURL}" alt="${escapeHTML(displayName)}" style="width:100%;height:100%;border-radius:50%;object-fit:cover;" onerror="this.parentElement.textContent='${escapeHTML(displayName.charAt(0).toUpperCase())}'">`;
    } else {
      userAvatar.textContent = displayName.charAt(0).toUpperCase();
    }

    // Load students for this user (connected to database and cloud storage)
    await loadStudentDashboard();
  } else {
    // Show Auth Page
    dashboardView.classList.add('hidden');
    authView.classList.remove('hidden');
  }
}

// ========================================================
// AUTH FORM SUBMISSIONS
// ========================================================

// 1. Email & Password Login
loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;

  btnLoginSubmit.disabled = true;
  btnLoginSubmit.querySelector('span').textContent = 'Signing in...';

  try {
    const user = await loginUser(email, password);
    showToast(`Welcome back, ${user.displayName || user.email}!`, 'success');
    handleAuthStateChanged(user);
  } catch (err) {
    showToast(err.message || 'Login failed. Please check credentials.', 'error');
  } finally {
    btnLoginSubmit.disabled = false;
    btnLoginSubmit.querySelector('span').textContent = 'Sign In to Dashboard';
  }
});

// 2. Registration
registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('register-name').value.trim();
  const email = document.getElementById('register-email').value.trim();
  const password = document.getElementById('register-password').value;
  const confirmPassword = document.getElementById('register-confirm-password').value;

  if (password !== confirmPassword) {
    showToast('Passwords do not match. Please verify.', 'error');
    return;
  }

  btnRegisterSubmit.disabled = true;
  btnRegisterSubmit.querySelector('span').textContent = 'Creating account...';

  try {
    const user = await registerUser(name, email, password);
    showToast(`Account created successfully! Welcome, ${user.displayName}.`, 'success');
    handleAuthStateChanged(user);
  } catch (err) {
    showToast(err.message || 'Registration failed.', 'error');
  } finally {
    btnRegisterSubmit.disabled = false;
    btnRegisterSubmit.querySelector('span').textContent = 'Create Account';
  }
});

// 3. Google Sign-In (powered by Auth0)
btnGoogleAuth.addEventListener('click', async () => {
  btnGoogleAuth.disabled = true;
  const originalSpan = btnGoogleAuth.querySelector('span');
  const originalText = originalSpan ? originalSpan.textContent : 'Continue with Google';
  if (originalSpan) originalSpan.textContent = 'Signing in with Google...';

  try {
    const user = await loginWithAuth0Google();
    if (user) {
      showToast(`Welcome back, ${user.displayName}!`, 'success');
      handleAuthStateChanged(user);
    }
  } catch (err) {
    console.error("Google login error:", err);
    showToast(err.message || 'Google sign-in was cancelled or failed.', 'error');
  } finally {
    btnGoogleAuth.disabled = false;
    if (originalSpan) originalSpan.textContent = originalText;
  }
});

// 4. Logout
btnLogout.addEventListener('click', async () => {
  try {
    if (currentUser && currentUser.provider === 'auth0') {
      await logoutAuth0();
    } else {
      await logoutUser();
    }
    showToast('You have been signed out.', 'info');
    handleAuthStateChanged(null);
  } catch (err) {
    showToast(err.message || 'Sign-out failed.', 'error');
  }
});

// ========================================================
// STUDENT DATA RENDERING & CRUD (FIREBASE STORAGE)
// ========================================================
async function loadStudentDashboard() {
  currentStudents = await getStudents();
  renderDashboard();
}

function renderDashboard() {
  updateKPIs();
  renderStudentTable();
}

function updateKPIs() {
  const total = currentStudents.length;
  const avgAge = total > 0 
    ? Math.round(currentStudents.reduce((sum, s) => sum + (parseInt(s.age, 10) || 0), 0) / total) 
    : 0;
  const uniqueDepts = new Set(currentStudents.map(s => s.department)).size;

  statTotalStudents.textContent = total;
  statAvgAge.textContent = `${avgAge} yrs`;
  statCoursesCount.textContent = uniqueDepts;
}

function getFilteredStudents() {
  const search = searchInput.value.toLowerCase().trim();
  const dept = courseFilter.value;

  return currentStudents.filter(student => {
    const matchesSearch = !search || 
      student.name.toLowerCase().includes(search) ||
      student.id.toLowerCase().includes(search) ||
      student.department.toLowerCase().includes(search);

    const matchesDept = !dept || student.department === dept;

    return matchesSearch && matchesDept;
  });
}

function renderStudentTable() {
  const filtered = getFilteredStudents();
  tableResultsCounter.textContent = `Showing ${filtered.length} of ${currentStudents.length} students`;

  if (filtered.length === 0) {
    studentTableBody.innerHTML = '';
    emptyStateView.style.display = 'block';
    return;
  }

  emptyStateView.style.display = 'none';

  studentTableBody.innerHTML = filtered.map(student => {
    const initials = student.name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();

    return `
      <tr>
        <td>
          <span style="font-weight: 700; font-family: monospace; font-size: 13.5px; color: var(--primary);">
            ${escapeHTML(student.id)}
          </span>
        </td>
        <td>
          <div class="student-name-cell">
            <div class="student-avatar">${initials}</div>
            <span class="student-meta-name">${escapeHTML(student.name)}</span>
          </div>
        </td>
        <td>
          <span style="font-weight: 600; color: #334155;">${escapeHTML(String(student.age))} yrs</span>
        </td>
        <td>
          <span class="badge-pill" style="${getDeptBadgeStyle(student.department)} font-weight: 600;">
            ${escapeHTML(student.department)}
          </span>
        </td>
        <td>
          <div class="action-buttons">
            <button type="button" class="btn-view-action" data-view-id="${student.id}" title="View Details">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
              <span>Details</span>
            </button>
            <button type="button" class="btn-delete-action" data-delete-id="${student.id}" title="Delete Student">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
              <span>Delete</span>
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join('');

  // Attach event handlers to view & delete buttons
  document.querySelectorAll('[data-view-id]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const id = e.currentTarget.getAttribute('data-view-id');
      handleViewStudent(id);
    });
  });

  document.querySelectorAll('[data-delete-id]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const id = e.currentTarget.getAttribute('data-delete-id');
      handlePromptDeleteStudent(id);
    });
  });
}

function escapeHTML(str) {
  if (!str) return '';
  return str.toString().replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}

function getDeptBadgeStyle(dept) {
  switch (dept) {
    case 'Computer Science':
      return 'background: #eef2ff; color: #4338ca; border: 1px solid #c7d2fe;';
    case 'Data Science':
      return 'background: #ecfeff; color: #0e7490; border: 1px solid #a5f3fc;';
    case 'Electrical Engineering':
      return 'background: #fffbeb; color: #b45309; border: 1px solid #fde68a;';
    case 'Business Administration':
      return 'background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0;';
    case 'Cybersecurity':
      return 'background: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff;';
    default:
      return 'background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1;';
  }
}

// Search and filter listeners
searchInput.addEventListener('input', renderStudentTable);
courseFilter.addEventListener('change', renderStudentTable);

// Add Student Modal triggers
function prepareAddStudentModal() {
  addStudentForm.reset();
  const nextNumber = Math.floor(100 + Math.random() * 900);
  document.getElementById('new-student-id').value = `STU-${nextNumber}`;
  openModal(modalAddStudent);
}

btnOpenAddStudent.addEventListener('click', prepareAddStudentModal);
btnEmptyAddStudent.addEventListener('click', prepareAddStudentModal);

// Add Student Form Submit (Stores in Firebase Storage)
addStudentForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const newStudentData = {
    id: document.getElementById('new-student-id').value.trim(),
    name: document.getElementById('new-student-name').value.trim(),
    age: parseInt(document.getElementById('new-student-age').value, 10),
    department: document.getElementById('new-student-dept').value
  };

  // Check if ID already exists
  if (currentStudents.some(s => s.id.toLowerCase() === newStudentData.id.toLowerCase())) {
    showToast(`A student with ID ${newStudentData.id} already exists.`, 'error');
    return;
  }

  const submitBtn = addStudentForm.querySelector('button[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Saving...';

  try {
    const saved = await addStudent(newStudentData);
    closeModal(modalAddStudent);
    showToast(`Student ${saved.name} added successfully!`, 'success');
    await loadStudentDashboard();
  } catch (err) {
    showToast(err.message || 'Failed to save student.', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Save Student Record';
  }
});

// Sync warning listener
window.addEventListener('firebase-sync-warning', (e) => {
  if (e.detail && e.detail.message) {
    showToast(e.detail.message, 'info');
  }
});

// View Student Details
function handleViewStudent(studentId) {
  const student = getStudentById(studentId);
  if (!student) return;

  const initials = student.name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();
  document.getElementById('detail-avatar').textContent = initials;
  document.getElementById('detail-name').textContent = student.name;
  document.getElementById('detail-id-badge').textContent = `ID: ${student.id}`;
  document.getElementById('detail-id').textContent = student.id;
  document.getElementById('detail-age').textContent = `${student.age} years old`;
  document.getElementById('detail-dept').textContent = student.department;

  openModal(modalViewStudent);
}

// Delete Student
function handlePromptDeleteStudent(studentId) {
  const student = getStudentById(studentId);
  if (!student) return;

  pendingDeleteStudentId = studentId;
  deleteStudentName.textContent = student.name;
  openModal(modalDeleteStudent);
}

btnConfirmDelete.addEventListener('click', async () => {
  if (!pendingDeleteStudentId) return;
  const removed = currentStudents.find(s => s.id === pendingDeleteStudentId);
  
  btnConfirmDelete.disabled = true;
  btnConfirmDelete.textContent = 'Deleting...';

  try {
    await deleteStudent(pendingDeleteStudentId);
    closeModal(modalDeleteStudent);
    showToast(`Removed student record ${removed ? removed.name : ''}.`, 'info');
    pendingDeleteStudentId = null;
    await loadStudentDashboard();
  } catch (err) {
    showToast(err.message || 'Failed to delete student.', 'error');
  } finally {
    btnConfirmDelete.disabled = false;
    btnConfirmDelete.textContent = 'Yes, Delete Record';
  }
});

// ========================================================
// FIREBASE CONFIGURATION MODAL & SETTINGS
// ========================================================
function populateFirebaseConfigInputs() {
  const config = getActiveFirebaseConfig();
  if (cfgApiKey) cfgApiKey.value = config.apiKey === 'YOUR_API_KEY' ? '' : (config.apiKey || '');
  if (cfgAuthDomain) cfgAuthDomain.value = config.authDomain.includes('YOUR_PROJECT_ID') ? '' : (config.authDomain || '');
  if (cfgProjectId) cfgProjectId.value = config.projectId === 'YOUR_PROJECT_ID' ? '' : (config.projectId || '');
  if (cfgAppId) cfgAppId.value = config.appId === 'YOUR_APP_ID' ? '' : (config.appId || '');
}

function populateAuth0ConfigInputs() {
  const config = getActiveAuth0Config();
  if (cfgAuth0Domain) {
    cfgAuth0Domain.value = (config.domain === 'dev-sample.us.auth0.com' || config.domain === 'YOUR_AUTH0_DOMAIN') 
      ? '' 
      : (config.domain || '');
  }
  if (cfgAuth0ClientId) {
    cfgAuth0ClientId.value = (config.clientId === 'YOUR_AUTH0_CLIENT_ID') 
      ? '' 
      : (config.clientId || '');
  }
}

function populateDropboxConfigInputs() {
  const config = getActiveDropboxConfig();
  if (cfgDropboxToken) {
    cfgDropboxToken.value = (config.accessToken === 'YOUR_DROPBOX_ACCESS_TOKEN') 
      ? '' 
      : (config.accessToken || '');
  }
  if (cfgDropboxPath) {
    cfgDropboxPath.value = config.filePath || '/students.json';
  }
}

function populateMongoConfigInputs() {
  const config = getActiveMongoConfig();
  if (cfgMongoDbName) {
    cfgMongoDbName.value = config.dbName || 'studentsphere_db';
  }
  if (cfgMongoCollection) {
    cfgMongoCollection.value = config.collectionName || 'students';
  }
}

function handleOpenSettings(e) {
  if (e) e.preventDefault();
  populateFirebaseConfigInputs();
  populateAuth0ConfigInputs();
  populateDropboxConfigInputs();
  populateMongoConfigInputs();
  openModal(modalFirebaseConfig);
}

btnOpenFirebaseConfig.addEventListener('click', handleOpenSettings);
btnNavFirebaseConfig.addEventListener('click', handleOpenSettings);
firebaseStatusPill.addEventListener('click', handleOpenSettings);

// Settings Tab Switching (Firebase vs Auth0 vs Dropbox vs MongoDB)
function switchSettingsTab(activeTab, activePanel) {
  const tabs = [tabCfgFirebase, tabCfgAuth0, tabCfgDropbox, tabCfgMongo];
  const panels = [panelCfgFirebase, panelCfgAuth0, panelCfgDropbox, panelCfgMongo];
  tabs.forEach(t => t && t.classList.remove('active'));
  panels.forEach(p => p && (p.style.display = 'none'));
  if (activeTab) activeTab.classList.add('active');
  if (activePanel) activePanel.style.display = 'block';
}

if (tabCfgFirebase) {
  tabCfgFirebase.addEventListener('click', () => switchSettingsTab(tabCfgFirebase, panelCfgFirebase));
}

if (tabCfgAuth0) {
  tabCfgAuth0.addEventListener('click', () => switchSettingsTab(tabCfgAuth0, panelCfgAuth0));
}

if (tabCfgDropbox) {
  tabCfgDropbox.addEventListener('click', () => switchSettingsTab(tabCfgDropbox, panelCfgDropbox));
}

if (tabCfgMongo) {
  tabCfgMongo.addEventListener('click', () => switchSettingsTab(tabCfgMongo, panelCfgMongo));
}

// Save Database Config
btnSaveFirebaseConfig.addEventListener('click', async () => {
  const newConfig = {
    apiKey: cfgApiKey.value.trim(),
    authDomain: cfgAuthDomain.value.trim(),
    projectId: cfgProjectId.value.trim(),
    storageBucket: `${cfgProjectId.value.trim()}.firebasestorage.app`,
    messagingSenderId: "",
    appId: cfgAppId.value.trim()
  };

  if (!newConfig.apiKey || !newConfig.projectId) {
    showToast('Please enter both an API Key and a Project ID.', 'error');
    return;
  }

  saveFirebaseConfig(newConfig);
  closeModal(modalFirebaseConfig);
  showToast('Database configuration saved! Reconnecting...', 'success');

  setTimeout(() => {
    window.location.reload();
  }, 1000);
});

// Reset Database Config
btnResetFirebaseConfig.addEventListener('click', () => {
  clearFirebaseConfig();
  populateFirebaseConfigInputs();
  showToast('Reset database settings to default.', 'info');
  setTimeout(() => {
    window.location.reload();
  }, 1000);
});

// Save SSO Config
if (btnSaveAuth0Config) {
  btnSaveAuth0Config.addEventListener('click', () => {
    const domain = cfgAuth0Domain ? cfgAuth0Domain.value.trim() : '';
    const clientId = cfgAuth0ClientId ? cfgAuth0ClientId.value.trim() : '';

    if (!domain || !clientId) {
      showToast('Please provide both SSO Domain and Client ID.', 'error');
      return;
    }

    saveAuth0Config({ domain, clientId });
    closeModal(modalFirebaseConfig);
    showToast('Single Sign-On configuration saved! Reloading...', 'success');

    setTimeout(() => {
      window.location.reload();
    }, 1000);
  });
}

// Reset SSO Config
if (btnResetAuth0Config) {
  btnResetAuth0Config.addEventListener('click', () => {
    clearAuth0Config();
    populateAuth0ConfigInputs();
    showToast('Reset Single Sign-On settings to default.', 'info');
  });
}

// Simulate SSO account trigger from Settings modal
if (btnDemoAuth0Trigger) {
  btnDemoAuth0Trigger.addEventListener('click', () => {
    closeModal(modalFirebaseConfig);
    const demoUser = loginWithAuth0Demo('Authorized Administrator', 'admin@university.edu');
    showToast('Signed in with test account!', 'success');
    handleAuthStateChanged(demoUser);
  });
}

// ========================================================
// DROPBOX STORAGE SETTINGS
// ========================================================
if (btnSaveDropboxConfig) {
  btnSaveDropboxConfig.addEventListener('click', () => {
    const accessToken = cfgDropboxToken ? cfgDropboxToken.value.trim() : '';
    const filePath = cfgDropboxPath ? cfgDropboxPath.value.trim() : '/students.json';

    if (!accessToken) {
      showToast('Please provide a Dropbox Access Token.', 'error');
      return;
    }

    saveDropboxConfig({ accessToken, filePath: filePath || '/students.json' });
    closeModal(modalFirebaseConfig);
    showToast('Dropbox configuration saved! Background syncing enabled.', 'success');
  });
}

if (btnResetDropboxConfig) {
  btnResetDropboxConfig.addEventListener('click', () => {
    clearDropboxConfig();
    populateDropboxConfigInputs();
    showToast('Reset Dropbox settings to default.', 'info');
  });
}

if (btnTestDropboxConfig) {
  btnTestDropboxConfig.addEventListener('click', async () => {
    const accessToken = cfgDropboxToken ? cfgDropboxToken.value.trim() : '';
    const filePath = cfgDropboxPath ? cfgDropboxPath.value.trim() : '/students.json';

    if (!accessToken) {
      showToast('Please enter an Access Token to test.', 'error');
      return;
    }

    // Persist temporarily for test
    saveDropboxConfig({ accessToken, filePath: filePath || '/students.json' });

    btnTestDropboxConfig.disabled = true;
    const prevText = btnTestDropboxConfig.textContent;
    btnTestDropboxConfig.textContent = 'Testing...';

    try {
      const res = await testDropboxConnection();
      showToast(`Connected to Dropbox! (${res.email || res.name})`, 'success');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      btnTestDropboxConfig.disabled = false;
      btnTestDropboxConfig.textContent = prevText;
    }
  });
}

// ========================================================
// MONGODB ATLAS SETTINGS
// ========================================================
if (btnTestMongoConfig) {
  btnTestMongoConfig.addEventListener('click', async () => {
    btnTestMongoConfig.disabled = true;
    const prevText = btnTestMongoConfig.textContent;
    btnTestMongoConfig.textContent = 'Connecting...';

    try {
      const res = await testMongoConnection();
      showToast(res.message || 'Connected to MongoDB Atlas successfully!', 'success');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      btnTestMongoConfig.disabled = false;
      btnTestMongoConfig.textContent = prevText;
    }
  });
}

if (btnSyncMongoNow) {
  btnSyncMongoNow.addEventListener('click', async () => {
    btnSyncMongoNow.disabled = true;
    const prevText = btnSyncMongoNow.textContent;
    btnSyncMongoNow.textContent = 'Syncing...';

    try {
      await syncAllStudentsToMongo(currentStudents);
      showToast(`Successfully synced ${currentStudents.length} students to MongoDB Atlas!`, 'success');
    } catch (err) {
      showToast(err.message || 'Could not sync to MongoDB Atlas', 'error');
    } finally {
      btnSyncMongoNow.disabled = false;
      btnSyncMongoNow.textContent = prevText;
    }
  });
}

// ========================================================
// INITIALIZATION
// ========================================================
async function initApp() {
  updateAuthStatusBadge();

  // 1. Check for incoming redirect callback (if redirected back with code & state)
  try {
    const redirectUser = await checkAuth0RedirectCallback();
    if (redirectUser) {
      showToast(`Welcome back, ${redirectUser.displayName}!`, 'success');
      await handleAuthStateChanged(redirectUser);
      return;
    }
  } catch (err) {
    showToast(err.message || 'Authentication error.', 'error');
  }

  // 2. Check for active session
  try {
    const auth0User = await checkAuth0Session();
    if (auth0User) {
      await handleAuthStateChanged(auth0User);
      return;
    }
  } catch (err) {
    console.warn("Session check:", err);
  }

  // 3. Initialize Authentication system
  await initializeAuthSystem(handleAuthStateChanged);
}

// Start app when DOM is ready
initApp();
