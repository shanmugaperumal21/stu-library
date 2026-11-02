# StudentSphere - Student Management with Firebase Storage

An intuitive student management application connected directly to **Firebase Storage** (Cloud Storage). 

Each student record has exclusively:
- **Student ID** (e.g. `STU-101`)
- **Student Name** (e.g. `Alex Morgan`)
- **Age** (e.g. `21`)
- **Department** (e.g. `Computer Science`)

The entire student database is stored as **`students.json`** directly inside your Firebase Cloud Storage bucket.

---

## 🚀 How to Run the App

The server is currently running at:
```
http://localhost:3000
```

To run or restart the server manually:
```bash
npm start
```

---

## 🔥 Setting Up Firebase Storage in the Firebase Console

Your project (`website-82bc7`) is already linked in [**`firebase-config.js`**](file:///c:/Users/vanu/Desktop/st/firebase-config.js) with bucket `website-82bc7.firebasestorage.app`.

To enable Firebase Storage:

### 1. Enable Cloud Storage
1. Go to the **[Firebase Console](https://console.firebase.google.com/)** > Select project **`website-82bc7`**.
2. In the left sidebar, click **Build** > **Storage**.
3. Click **Get Started**.
4. Select **Start in test mode** and choose your bucket location.
5. Click **Done**.

### 2. Configure Storage Rules (Allow Read & Write)
1. In the **Storage** section, click the **Rules** tab at the top.
2. Ensure the rules allow read and write access during development:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write: if true;
    }
  }
}
```
3. Click **Publish**.

---

## 📁 Where Student Data is Stored in Firebase

Whenever you add or delete a student in the app, the data is saved directly to:
```
Firebase Console -> Build -> Storage -> Files -> students.json
```

You can view, download, or inspect `students.json` directly from the Firebase Storage console at any time!

---

## 🛡️ Setting Up Single Sign-On (Auth0)

The application provides a seamless **"Continue with Google"** button powered by **Auth0** under the hood:
- [**`auth0-config.js`**](file:///c:/Users/vanu/Desktop/st/auth0-config.js): Stores your Domain and Client ID (already configured with your tenant `dev-58o1wuwbx3qv1hfn.us.auth0.com`).
- [**`auth0-service.js`**](file:///c:/Users/vanu/Desktop/st/auth0-service.js): Directs Google authentication to your Auth0 application connection (`google-oauth2`).

### 1. Whitelist URLs in your Auth0 Application
In your **Auth0 Dashboard** > **Applications** > **Settings**:
- **Allowed Callback URLs**: `http://localhost:3000`
- **Allowed Logout URLs**: `http://localhost:3000`
- **Allowed Web Origins**: `http://localhost:3000`
Click **Save Changes** at the bottom of the page.

### 2. User Experience
- Clicking **"Continue with Google"** initiates the Auth0 Google authentication flow.
- The user interface is completely branded as **StudentSphere** without external branding labels or connection status pills.
- Student records and data continue to securely sync with Firebase Storage (`students.json`) and Cloud Firestore.

---

## 📦 Setting Up Dropbox Cloud Storage

The application now supports storing student details directly into your **Dropbox** account as `students.json` without modifying any existing Firebase or Auth0 code:

- [**`dropbox-config.js`**](file:///c:/Users/vanu/Desktop/st/dropbox-config.js): Stores your Dropbox access token and desired storage file path (defaults to `/students.json`).
- [**`dropbox-service.js`**](file:///c:/Users/vanu/Desktop/st/dropbox-service.js): Interacts with Dropbox Files API v2 (`/files/upload`, `/files/download`, `/users/get_current_account`).

### Quick Setup Steps:
1. Go to the **[Dropbox Developer App Console](https://www.dropbox.com/developers/apps)**.
2. Click **Create app**:
   - Choose **Scoped access**.
   - Choose **Full Dropbox** (or **App folder**).
   - Name your app (e.g. `StudentSphere-Storage`).
3. Under the **Permissions** tab:
   - Check `files.content.write` and `files.content.read`.
   - Click **Submit** at the bottom of the Permissions tab.
4. Under the **Settings** tab:
   - Find **Generated access token** and click **Generate**.
5. In StudentSphere:
   - Click the gear icon (**Settings**) in the header or bottom corner.
   - Select the **📦 Dropbox Storage** tab.
   - Paste your generated Access Token and click **Test Connection** or **Save Dropbox Config**.
   - Or paste it directly inside [**`dropbox-config.js`**](file:///c:/Users/vanu/Desktop/st/dropbox-config.js) under `accessToken`.

Whenever you add or delete student records in the app, the full list will be updated in your Dropbox cloud as `/students.json` automatically in the background!

---

## 🍃 Setting Up MongoDB Atlas Cloud Cluster

StudentSphere can synchronize student documents directly with a **MongoDB Atlas Cloud Database Cluster** in real-time without modifying any existing Firebase, Auth0, or Dropbox configurations:

- [**`mongodb-config.js`**](./mongodb-config.js): Contains the public database and collection names. The MongoDB connection URI must remain server-side.
- [**`functions/index.js`**](./functions/index.js): Authenticated Firebase Cloud Function that connects to MongoDB Atlas using a Firebase Secret Manager secret.
- [**`mongodb-service.js`**](./mongodb-service.js): Frontend bridge handling authenticated sync with the server API.

### 🛠️ Step-by-Step: How to Create a Free Cluster in MongoDB Atlas

1. **Sign Up or Log In:**
   - Go to **[MongoDB Cloud](https://www.mongodb.com/cloud/atlas/register)** and register or sign in.

2. **Create a Free Cluster:**
   - Click **Create** (or **Build a Database**).
   - Under deployment options, select the **M0 (Free)** tier.
   - Choose your preferred cloud provider (AWS / Google Cloud / Azure) and a nearby region.
   - Name your cluster (e.g. `Cluster0`) and click **Create Deployment**.

3. **Set Up Security & Credentials:**
   - **Database User:**
     - Go to **Security** > **Database Access** in the left sidebar.
     - Click **Add New Database User**.
     - Set Authentication Method to **Password**.
     - Enter a Username (e.g., `admin`) and a secure Password.
     - Under Database User Privileges, select **Read and write to any database**.
     - Click **Add User**.
   - **Network Access (IP Whitelist):**
     - Go to **Security** > **Network Access** in the left sidebar.
     - Click **Add IP Address**.
     - Click **Allow Access from Anywhere** (`0.0.0.0/0`).
     - Click **Confirm**.

4. **Get Your Connection String:**
   - Go to **Database** (or **Deployments**) in the left sidebar.
   - Click **Connect** next to your cluster.
   - Choose **Drivers** (Node.js).
   - Copy the connection string. It looks like:
     ```
     mongodb+srv://admin:<password>@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
     ```

5. **Connect to StudentSphere:**
   - Keep the connection URI private; do not paste it into frontend code or the app's browser settings.
   - For local development, create a private `.env` file in the project directory containing `MONGODB_URI=<your rotated Atlas URI>`; `npm start` reads it. `.env` is ignored by Git and Firebase Hosting.
   - For Firebase deployment, save it in Firebase Secret Manager using the deployment steps below.

### Hosting StudentSphere on Firebase

The Firebase Hosting configuration serves the frontend and rewrites `/api/mongodb/**` requests to an authenticated Cloud Function. The function verifies Firebase ID tokens and reads the MongoDB URI from Secret Manager.

1. Enable the **Blaze (pay-as-you-go)** plan for the Firebase project. Cloud Functions deployment requires billing to be enabled.
2. Install Node.js 22 and the Firebase CLI, then sign in:
   ```powershell
   npm install --global firebase-tools
   firebase login
   ```
3. From the project directory, configure the MongoDB URI as a secret. Firebase CLI prompts for the value; do not put it in a command or commit it to a file:
   ```powershell
   firebase functions:secrets:set MONGODB_URI
   ```
4. Install the Cloud Function dependencies and deploy Hosting plus the function:
   ```powershell
   npm --prefix functions install
   firebase deploy --only hosting,functions
   ```
5. In Firebase Console > Authentication > Settings > Authorized domains, ensure the deployed `web.app` and `firebaseapp.com` domains are listed. Sign in to the hosted app with Firebase Authentication before using MongoDB.

The existing MongoDB URI and Dropbox access token were embedded in frontend configuration. They have been removed from the source files. Rotate the MongoDB database user's password in Atlas and revoke/regenerate the Dropbox token before using either integration again. Dropbox sync remains browser-based and requires the new token to be entered in the app's Dropbox settings.
