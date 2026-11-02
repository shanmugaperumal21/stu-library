# -*- coding: utf-8 -*-
"""
HTML and PDF Report Generator for StudentSphere
Creates an exact 23-page academic report layout matching the sample report template.
"""

import os
import subprocess

WORKSPACE = r"e:\st-20261015T083357Z-1-001"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>StudentSphere - Cloud Computing Laboratory Project Report</title>
<style>
  @page {
    size: A4 portrait;
    margin: 22mm 20mm 22mm 20mm;
    @bottom-center {
      content: counter(page);
      font-size: 10pt;
      font-family: 'Times New Roman', Times, serif;
    }
  }

  *, *:before, *:after {
    box-sizing: border-box;
  }

  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 11.5pt;
    line-height: 1.45;
    color: #111111;
    margin: 0;
    padding: 0;
    background: #ffffff;
  }

  .page {
    page-break-after: always;
    min-height: 250mm;
    position: relative;
    padding: 5mm 0;
  }

  /* Cover Page Styling */
  .cover-page {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    min-height: 255mm;
    padding: 25mm 10mm 15mm 10mm;
  }

  .cover-title {
    font-size: 24pt;
    font-weight: bold;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
    color: #000000;
  }

  .cover-subtitle {
    font-size: 13pt;
    font-weight: 500;
    margin-bottom: 22px;
    color: #222222;
  }

  .cover-report-tag {
    font-size: 12.5pt;
    font-weight: bold;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
    color: #000000;
  }

  .cover-course-code {
    font-size: 13pt;
    font-weight: bold;
    margin-bottom: 30px;
    color: #000000;
  }

  .cover-submitted-label {
    font-size: 12pt;
    font-style: italic;
    margin-bottom: 25px;
    color: #333333;
  }

  .cover-team-box {
    margin-bottom: 40px;
    line-height: 1.8;
  }

  .cover-student-name {
    font-size: 11.5pt;
    font-weight: bold;
    color: #000000;
  }

  .cover-reg-num {
    font-weight: normal;
  }

  .cover-bottom-box {
    font-size: 11pt;
    line-height: 1.6;
    color: #111111;
  }

  .cover-dept {
    font-weight: bold;
    margin-top: 15px;
    font-size: 12pt;
  }

  .cover-college {
    font-size: 11.5pt;
    margin-top: 4px;
  }

  .cover-year {
    font-size: 11.5pt;
    margin-top: 6px;
    font-weight: 500;
  }

  /* Headings */
  h1 {
    font-size: 14pt;
    font-weight: bold;
    margin-top: 0;
    margin-bottom: 12px;
    color: #000000;
  }

  h2 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 14px;
    margin-bottom: 6px;
    color: #000000;
  }

  h3 {
    font-size: 11.5pt;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 4px;
    color: #111111;
  }

  p {
    margin-top: 0;
    margin-bottom: 10px;
    text-align: justify;
    text-justify: inter-word;
  }

  ul, ol {
    margin-top: 0;
    margin-bottom: 10px;
    padding-left: 24px;
  }

  li {
    margin-bottom: 4px;
    text-align: justify;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 9.5pt;
  }

  th, td {
    border: 1px solid #333333;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
  }

  th {
    background-color: #f1f5f9;
    font-weight: bold;
    color: #000000;
  }

  tr:nth-child(even) td {
    background-color: #fafafa;
  }

  /* Code & Snippets */
  pre {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 8px 12px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.35;
    margin: 8px 0 12px 0;
    white-space: pre-wrap;
    word-break: break-all;
  }

  code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
  }

  /* Figures */
  .figure-container {
    text-align: center;
    margin: 14px 0;
  }

  .figure-img {
    max-width: 95%;
    max-height: 120mm;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }

  .figure-caption {
    font-style: italic;
    font-size: 9.5pt;
    margin-top: 6px;
    color: #222222;
  }

  .italic-note {
    font-style: italic;
    font-size: 10pt;
    color: #444444;
    margin: 8px 0 16px 0;
  }

  .badge-keyword {
    font-weight: bold;
  }
</style>
</head>
<body>

<!-- ========================================== -->
<!-- PAGE 1: TITLE PAGE                         -->
<!-- ========================================== -->
<div class="page cover-page">
  <div>
    <div class="cover-title">STUDENTSPHERE</div>
    <div class="cover-subtitle">A Multi-Cloud Student Management and Academic Records Platform</div>
    <div class="cover-report-tag">CLOUD COMPUTING LABORATORY PROJECT REPORT</div>
    <div class="cover-course-code">(22IT580)</div>
  </div>

  <div class="cover-team-box">
    <div class="cover-submitted-label">Submitted by</div>
    <p class="cover-student-name">SHANMUGA PERUMAL A — <span class="cover-reg-num">Register Number: 2403917720521313</span></p>
    <p class="cover-student-name">VANAMAMALAI M — <span class="cover-reg-num">Register Number: 2403917720521086</span></p>
    <p class="cover-student-name">EDWIN MOSES G — <span class="cover-reg-num">Register Number: 2403917720521305</span></p>
  </div>

  <div class="cover-bottom-box">
    <p>Submitted in partial fulfilment of the requirements for the Cloud Computing Laboratory</p>
    <p class="cover-dept">Department of Information Technology</p>
    <p class="cover-college">Thiagarajar College of Engineering, Madurai</p>
    <p class="cover-year">Academic Year: 2026–2027</p>
  </div>
</div>


<!-- ========================================== -->
<!-- PAGE 2: ABSTRACT & TABLE OF CONTENTS       -->
<!-- ========================================== -->
<div class="page">
  <h1>Abstract</h1>
  <p>
    StudentSphere is a full-stack, cloud-native student information and directory management platform developed to let academic institutions and faculty administrators store, organize, search, filter, and backup student records across hybrid multi-cloud environments. The application demonstrates how several cloud service models can be harmoniously combined in a single institutional platform: Identity as a Service (IDaaS), Database as a Service (DBaaS), Backend as a Service (BaaS), and Storage as a Service (STaaS).
  </p>
  <p>
    The frontend is an intuitive Single Page Application (SPA) built with HTML5, vanilla CSS3 featuring modern glassmorphic aesthetics, and JavaScript ES modules. It communicates with an extensible Node.js HTTP backend server and Google Cloud Firebase Cloud Functions. Auth0 is employed for Identity as a Service (IDaaS) with Universal Login and Google OAuth 2.0 federation. MongoDB Atlas provides managed Database as a Service (DBaaS) for structured document persistence, while Google Firebase Cloud Firestore serves as Backend as a Service (BaaS) providing real-time data synchronization. Firebase Cloud Storage and the Dropbox API v2 supply Storage as a Service (STaaS) for instant cloud object persistence and automated JSON cloud backup.
  </p>
  <p>
    Administrators can create, view, search, and delete student records, filter the roster by academic department, inspect detailed demographic attributes, and initiate one-click synchronization to Dropbox cloud storage and MongoDB Atlas. Authentication middleware and token validation ensure that only authorized administrative users can access and modify student records.
  </p>
  <p>
    The main objective of the project is to demonstrate the practical integration of multiple independent cloud platforms, each chosen for a specific responsibility, rather than relying on a single vendor or a vulnerable local desktop system. The project provides hands-on experience in REST API development, serverless microservice design, token-based authentication, NoSQL document databases, real-time data streaming, and automated cloud file synchronization.
  </p>
  <p>
    <span class="badge-keyword">Keywords:</span> Cloud Computing, StudentSphere, Multi-Cloud Integration, Auth0, MongoDB Atlas, Firebase Firestore, Firebase Storage, Dropbox API, IDaaS, DBaaS, BaaS, STaaS.
  </p>

  <h1 style="margin-top: 20px;">Table of Contents</h1>
  <ol>
    <li>Introduction</li>
    <li>Problem Statement</li>
    <li>Objectives</li>
    <li>Existing System</li>
    <li>Proposed System</li>
    <li>System Requirements</li>
    <li>Technologies Used</li>
    <li>System Architecture</li>
    <li>System Design and Modules</li>
    <li>Implementation</li>
    <li>Application Screenshots and Results</li>
    <li>Testing and Results</li>
    <li>Advantages</li>
    <li>Limitations</li>
  </ol>
</div>


<!-- ========================================== -->
<!-- PAGE 3: TOC CONT. & 1. INTRODUCTION       -->
<!-- ========================================== -->
<div class="page">
  <ol start="15">
    <li>Future Enhancements</li>
    <li>Conclusion</li>
    <li>References</li>
  </ol>
  <p class="italic-note">Note: update the page numbers after the final formatting.</p>

  <h1>1. Introduction</h1>
  <p>
    Cloud computing is a technology that provides computing resources such as storage, databases, servers, identity services, and software through the internet. It allows applications to use these resources on demand without maintaining all the required infrastructure locally.
  </p>
  <p>
    Academic institutions, universities, and departmental offices regularly maintain large volumes of student records, including Student IDs, full names, age demographics, and department affiliations. Traditionally, these records are scattered across localized spreadsheets, personal office computers, disparate flat files, or single-vendor proprietary systems, making them difficult to locate, share securely, and backup against hardware failure.
  </p>
  <p>
    StudentSphere is designed to provide a centralized, secure platform for managing student records through modern cloud services. It combines enterprise identity federation, multiple database backends, and cloud file storage in one application, ensuring that institutional data is always accessible, resilient, and synchronized across departments.
  </p>
  <p>
    The application follows a decoupled, multi-tier architecture. A modern Single Page Application provides the user interface. A Node.js HTTP server handles REST API endpoints and static file serving, while Google Cloud Firebase Cloud Functions execute serverless database operations with Secret Manager credential protection.
  </p>
  <p>
    Auth0 is responsible for user identity and authentication. MongoDB Atlas and Firebase Firestore store structured student records. Dropbox API v2 and Firebase Cloud Storage provide cloud object storage in which student rosters are saved as persistent JSON datasets.
  </p>
  <p>
    The integration of these services demonstrates how multiple cloud platforms can work together in a practical application. The project also introduces vital cloud concepts such as OAuth 2.0 and OpenID Connect, JSON Web Tokens (JWT), managed NoSQL clusters, real-time WebSocket listeners, and multi-cloud disaster recovery.
  </p>

  <h2>1.1 Need for the Project</h2>
  <p>Academic administrators and faculty members need fast, secure access to student records from any device. The need for the project includes:</p>
  <ul>
    <li>Providing authenticated, institutional access to centralized student databases.</li>
    <li>Storing student records in managed cloud databases instead of volatile local files.</li>
    <li>Eliminating single-vendor lock-in by distributing workloads across independent cloud providers.</li>
    <li>Providing instant live search and department-level filtering across all student records.</li>
    <li>Automating offsite cloud backups to personal or institutional Dropbox storage.</li>
    <li>Demonstrating the simultaneous integration of IDaaS, DBaaS, BaaS, and STaaS in a single academic portal.</li>
  </ul>
</div>


<!-- ========================================== -->
<!-- PAGE 4: 1.2 SCOPE, 2. PROBLEM, 3. OBJECTIVES-->
<!-- ========================================== -->
<div class="page">
  <h2>1.2 Scope of the Project</h2>
  <p>
    The scope of StudentSphere includes secure administrative authentication, student record creation, retrieval, viewing, updating, and deletion (CRUD), multi-cloud storage synchronization through Firestore and MongoDB Atlas, and automated cloud file export to Dropbox and Firebase Cloud Storage. The application is intended as an academic implementation and demonstration of cloud computing paradigms.
  </p>

  <h1>2. Problem Statement</h1>
  <p>
    Educational institutions keep student records in many disparate locations, including desktop spreadsheet applications, local text files, and isolated office workstations. When student details are stored separately across faculty desks, searching for records, updating student details, and aggregating departmental rosters becomes inconvenient, slow, and prone to data discrepancies.
  </p>
  <p>
    Local storage also severely limits access when faculty members work from different terminals, lecture halls, or remote locations. Furthermore, relying on a single storage backend creates critical vendor lock-in; a service disruption from that provider completely halts institutional operations. Managing user access safely, preserving data privacy, and generating usable data backups typically requires extensive manual effort and third-party software.
  </p>
  <p>
    Therefore, a cloud-based student management platform is needed that combines secure authentication, flexible multi-database storage, real-time synchronization, and automated cloud file export in one cohesive application. StudentSphere solves this challenge by integrating Auth0, MongoDB Atlas, Firebase Cloud Firestore, Firebase Storage, and Dropbox through an intuitive web client, a Node.js REST server, and serverless Cloud Functions.
  </p>

  <h1>3. Objectives</h1>
  <p>
    The primary objective is to develop a cloud-native application that demonstrates the practical integration of multiple cloud service models. The specific objectives are:
  </p>
  <ol>
    <li>To develop a responsive Single Page Application using HTML5, modern CSS3 with glassmorphism styling, and vanilla JavaScript ES modules.</li>
    <li>To develop a backend REST API using Node.js for MongoDB Atlas integration and static asset serving.</li>
    <li>To implement user authentication and Google Single Sign-On using Auth0 Identity Platform.</li>
    <li>To store student documents in MongoDB Atlas as a managed cloud database (DBaaS).</li>
    <li>To use Firebase Cloud Firestore for real-time reactive synchronization of student records across connected clients.</li>
    <li>To provide persistent object storage in Firebase Cloud Storage as <code>students.json</code>.</li>
    <li>To integrate the Dropbox API v2 for offsite cloud backup and disaster recovery.</li>
    <li>To provide resilient optimistic UI updates backed by browser local storage caching.</li>
    <li>To test and evaluate the communication and fault tolerance between the application and external cloud services.</li>
  </ol>

  <h2>3.1 Project Outcomes</h2>
  <ul>
    <li>An interactive administrative portal for creating, viewing, searching, and deleting student profiles.</li>
    <li>Authentication-based access control protecting student records from unauthorized access.</li>
    <li>Real-time data streaming where database updates reflect immediately on all client screens without refreshing.</li>
    <li>Hybrid data persistence across MongoDB Atlas, Firebase Firestore, and Firebase Cloud Storage.</li>
    <li>Direct-to-cloud automated backup snapshots into Dropbox as <code>/students.json</code>.</li>
  </ul>
</div>


<!-- ========================================== -->
<!-- PAGE 5: 4. EXISTING, 5. PROPOSED SYSTEM    -->
<!-- ========================================== -->
<div class="page">
  <h1>4. Existing System</h1>
  <p>
    In a traditional institutional setup, departments manage student records using localized spreadsheet files (e.g., Microsoft Excel), local CSV/JSON files, or on-premise desktop database management systems (such as local MS Access or standalone MySQL instances). Each department maintains its own files independently, requiring administrative personnel to manually reconcile rosters, email copies between offices, and manage their own local backups.
  </p>

  <h2>4.1 Disadvantages of the Existing System</h2>
  <ul>
    <li>Student records are scattered across multiple office workstations and departmental folders.</li>
    <li>Access is strictly dependent on the physical device where the files are stored.</li>
    <li>Searching across student IDs, names, and departments is cumbersome across multiple files.</li>
    <li>User access control, password security, and student data confidentiality are difficult to enforce.</li>
    <li>A single storage provider or hard drive failure causes catastrophic and permanent data loss.</li>
    <li>Exporting student rosters to cloud storage is a tedious, manual process prone to human error.</li>
    <li>Integrating multiple independent cloud services manually requires significant engineering overhead.</li>
  </ul>

  <h1>5. Proposed System</h1>
  <p>
    The proposed StudentSphere system provides a centralized web application that seamlessly unites authentication, real-time database, managed cloud cluster, and distributed cloud file storage services into a cohesive portal.
  </p>
  <p>
    Auth0 manages identity authentication and token issuance through OpenID Connect and Google OAuth federation. The web client communicates directly with Google Firebase Cloud Firestore via real-time reactive listeners (<code>onSnapshot</code>), ensuring that updates appear instantly on all active screens without manual browser refreshes. Concurrently, records are persisted into Google Firebase Cloud Storage as <code>students.json</code>.
  </p>
  <p>
    For structured database persistence, the application routes data through a Node.js REST API to MongoDB Atlas (DBaaS). An integrated Dropbox module interfaces directly with Dropbox Files API v2 to save student rosters as standalone cloud backup files.
  </p>

  <h2>5.1 Advantages of the Proposed System</h2>
  <ul>
    <li>Centralized administrative portal accessible from any desktop or mobile web browser.</li>
    <li>Authentication-based access control and secure token validation.</li>
    <li>Zero UI latency through optimistic client-side caching.</li>
    <li>Real-time, reactive roster updates across all active sessions without manual polling.</li>
    <li>Automated export and offsite cloud backup of student records to Dropbox.</li>
    <li>Multi-cloud resilience that eliminates vendor lock-in by utilizing Google Cloud, MongoDB Atlas, and Dropbox in parallel.</li>
    <li>Decoupled, modular architecture supporting independent scaling and straightforward maintenance.</li>
  </ul>
</div>


<!-- ========================================== -->
<!-- PAGE 6: 5.2 COMPARISON & 6. REQUIREMENTS   -->
<!-- ========================================== -->
<div class="page">
  <h2>5.2 Comparison</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 45%;">Existing Approach</th>
        <th style="width: 55%;">Proposed StudentSphere Approach</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Student records are stored in local spreadsheet files or on-premise desktops.</td>
        <td>Records are stored simultaneously across MongoDB Atlas, Firestore, and Cloud Storage.</td>
      </tr>
      <tr>
        <td>Only one local storage location is used, risking complete data loss.</td>
        <td>Multi-cloud hybrid storage ensures continuous redundancy and disaster recovery.</td>
      </tr>
      <tr>
        <td>Separate, unencrypted passwords or shared credentials must be maintained.</td>
        <td>Enterprise IDaaS via Auth0 is integrated for Universal Login and Google SSO.</td>
      </tr>
      <tr>
        <td>Changes require manual refreshing, emailing files, or periodic re-importing.</td>
        <td>Firebase Firestore real-time listeners update the interface instantaneously.</td>
      </tr>
      <tr>
        <td>Files are backed up manually to USB flash drives or external drives.</td>
        <td>Student datasets are automatically synchronized to Dropbox as <code>/students.json</code>.</td>
      </tr>
      <tr>
        <td>Cloud services operate in silos or are not utilized at all.</td>
        <td>Four cloud service models (IDaaS, DBaaS, BaaS, STaaS) operate in harmony.</td>
      </tr>
    </tbody>
  </table>

  <h1>6. System Requirements</h1>
  <p>
    The application requires a computer capable of executing Node.js and a modern browser with internet connectivity. Cloud accounts must be configured with active credentials before corresponding functions operate.
  </p>

  <h2>6.1 Hardware Requirements</h2>
  <ul>
    <li>Computer or laptop (Intel Core i3 / AMD Ryzen 3 or higher).</li>
    <li>Minimum 4 GB RAM recommended (8 GB preferred).</li>
    <li>Sufficient disk space for Node.js modules and dependencies (at least 500 MB free).</li>
    <li>Active internet connection (minimum 1 Mbps).</li>
    <li>Keyboard, pointing device, and display monitor (1080p resolution recommended).</li>
  </ul>

  <h2>6.2 Software Requirements</h2>
  <ul>
    <li>Operating System: Windows 10/11, macOS, or Linux.</li>
    <li>Runtime Environment: Node.js (v18.x, v20.x, or v22.x LTS).</li>
    <li>Package Manager: npm (v9.x or higher).</li>
    <li>Frontend Technologies: HTML5, CSS3 with glassmorphism styling, and JavaScript ES Modules.</li>
    <li>Backend Server: Node.js native HTTP server and Firebase Cloud Functions (2nd Gen).</li>
    <li>Authentication Service: Auth0 by Okta.</li>
    <li>Database Services: MongoDB Atlas (M0 Free Tier) and Google Cloud Firestore.</li>
    <li>Cloud Storage Services: Google Firebase Storage and Dropbox API v2.</li>
    <li>Development Tools: Visual Studio Code, Git CLI, and modern web browser (Chrome or Edge).</li>
  </ul>
</div>


<!-- ========================================== -->
<!-- PAGE 7: 6.3 FUNCTIONAL & 7. TECHNOLOGIES   -->
<!-- ========================================== -->
<div class="page">
  <h2>6.3 Functional Requirements</h2>
  <ol>
    <li>Authenticate users securely through Auth0 (institutional email/password or Google SSO).</li>
    <li>Validate identity claims and maintain persistent authenticated user sessions.</li>
    <li>Create student records with unique Student ID, Full Name, Age, and Department.</li>
    <li>Display student records in an interactive, responsive data table with status indicators.</li>
    <li>Update student records and render modifications immediately across all clients.</li>
    <li>Delete student records from selected cloud storage engines with safety confirmation.</li>
    <li>Provide real-time multi-field search across Student ID, Name, and Department.</li>
    <li>Filter student rosters dynamically by selecting specific academic departments.</li>
    <li>Synchronize student datasets to Google Firebase Storage as <code>students.json</code>.</li>
    <li>Export and backup student records to personal Dropbox accounts via Dropbox API v2.</li>
    <li>Report cloud service connection statuses and diagnostics through the system settings modal.</li>
  </ol>

  <h2>6.4 Non-Functional Requirements</h2>
  <ul>
    <li><strong>Security:</strong> Protected administrative operations require valid authentication; sensitive database connection strings are stored server-side in Secret Manager.</li>
    <li><strong>Reliability:</strong> Multi-engine architecture ensures that failure in one cloud service does not prevent access through secondary engines.</li>
    <li><strong>Usability:</strong> The interface provides intuitive live search, color-coded department tags, clear visual hierarchy, and non-blocking toast notifications.</li>
    <li><strong>Maintainability:</strong> The frontend SPA, Node.js API server, and Cloud Functions are decoupled into modular ES modules.</li>
    <li><strong>Performance:</strong> Initial page load completes in under 1.5 seconds; local optimistic updates render in under 50 milliseconds.</li>
  </ul>

  <h1>7. Technologies Used</h1>
  <h2>7.1 Frontend Architecture (HTML5, Vanilla CSS, ES Modules)</h2>
  <p>
    The frontend is constructed using pure HTML5, modern CSS3, and JavaScript ES modules. By avoiding heavy UI framework dependencies, the application achieves lightning-fast load times. The interface is styled with custom modern CSS utilizing CSS Custom Properties, backdrop-filter glassmorphism, flexbox and grid layouts, and smooth micro-animations.
  </p>

  <h2>7.2 Node.js HTTP Runtime and Firebase Cloud Functions</h2>
  <p>
    Node.js is used to execute server-side JavaScript outside the browser. A native Node.js HTTP server (<code>server.js</code>) on port 3000 handles static asset delivery and REST endpoints at <code>/api/mongodb/*</code>. In cloud deployments, Google Firebase Cloud Functions (2nd Gen) provide serverless REST endpoints with Secret Manager integration.
  </p>
</div>


<!-- ========================================== -->
<!-- PAGE 8: 7.3 - 7.9 TECHNOLOGIES CONT.        -->
<!-- ========================================== -->
<div class="page">
  <h2>7.3 Auth0 Identity Platform</h2>
  <p>
    Auth0, by Okta, is an enterprise identity platform that handles user registration, login, session token issuance, and social OAuth federation. In StudentSphere, the frontend uses the <code>@auth0/auth0-spa-js</code> library and Universal Login based on OpenID Connect (OIDC). Users authenticate with institutional email credentials or through Google Single Sign-On (<code>google-oauth2</code> connection).
  </p>

  <h2>7.4 Google Firebase Cloud Firestore</h2>
  <p>
    Firebase Cloud Firestore is a serverless NoSQL document database featuring real-time data synchronization. The web client uses the Firebase modular SDK (v10.12.0) and <code>onSnapshot</code> listeners to subscribe to the <code>students</code> collection, updating the UI instantly whenever records are added, modified, or removed.
  </p>

  <h2>7.5 Google Firebase Cloud Storage</h2>
  <p>
    Firebase Cloud Storage is an enterprise object storage service backed by Google Cloud Storage. In StudentSphere, the complete student roster is serialized and stored in bucket <code>website-82bc7.firebasestorage.app</code> as a persistent <code>students.json</code> file.
  </p>

  <h2>7.6 MongoDB Atlas</h2>
  <p>
    MongoDB Atlas is a fully managed cloud NoSQL document database. The Node.js backend connects to MongoDB Atlas using the official <code>mongodb</code> driver (v7.7.0) via a <code>mongodb+srv://</code> connection string with DNS SRV record discovery. Records are stored as structured documents in database <code>studentsphere_db</code> under collection <code>students</code>.
  </p>

  <h2>7.7 Dropbox API v2</h2>
  <p>
    Dropbox provides cloud file storage and an HTTP REST API for file operations. StudentSphere interfaces directly with Dropbox Files API v2 endpoints (<code>/2/files/upload</code> and <code>/2/users/get_current_account</code>) using OAuth 2.0 bearer tokens to save student backups to <code>/students.json</code>.
  </p>

  <h2>7.8 npm and Package Ecosystem</h2>
  <p>
    npm manages backend dependencies such as the official <code>mongodb</code> driver and <code>firebase-admin</code>. npm scripts allow starting the local development server with environment variables loaded automatically.
  </p>

  <h2>7.9 Environment Variables and Configuration Security</h2>
  <p>
    Environment variables store sensitive configuration values such as server ports, Auth0 credentials, Firebase configuration keys, and the MongoDB connection URI. Sensitive credentials are kept in a private <code>.env</code> file locally and stored in Google Secret Manager for production deployments, ensuring they are never exposed in public repositories or screenshots.
  </p>
</div>


<!-- ========================================== -->
<!-- PAGE 9: 8. SYSTEM ARCHITECTURE             -->
<!-- ========================================== -->
<div class="page">
  <h1>8. System Architecture</h1>
  <p>
    StudentSphere follows a decoupled, multi-tier architecture in which a lightweight single-page frontend communicates with dedicated backend services and four independent public cloud platforms.
  </p>

  <h2>8.1 Architecture Components</h2>
  <ol>
    <li><strong>Client Presentation Tier:</strong> The HTML5/CSS3/JavaScript SPA running on port 3000. It handles state management, optimistic UI updates, and reactive cloud listeners.</li>
    <li><strong>Node.js HTTP Server & Cloud Functions:</strong> The backend compute engine serving static files and REST endpoints at <code>/api/mongodb/*</code>.</li>
    <li><strong>Auth0 Identity Platform (IDaaS):</strong> Manages institutional authentication, issuing signed JWT tokens and handling Google OAuth federation.</li>
    <li><strong>Firebase Cloud Firestore (BaaS):</strong> Stores real-time student collections with continuous client stream listeners.</li>
    <li><strong>Firebase Cloud Storage (STaaS):</strong> Hosts persistent cloud object files (<code>students.json</code>) in Google Cloud.</li>
    <li><strong>MongoDB Atlas (DBaaS):</strong> Stores structured NoSQL student documents in cloud database <code>studentsphere_db</code>.</li>
    <li><strong>Dropbox API v2 (STaaS):</strong> Stores automated offsite disaster recovery backup files in Dropbox cloud accounts.</li>
  </ol>

  <h2>8.2 Architecture Diagram</h2>
  <div class="figure-container">
    <img class="figure-img" src="fig_architecture.png" alt="Architecture of StudentSphere">
    <div class="figure-caption">Figure 1: Multi-Cloud Architecture of StudentSphere.</div>
  </div>

  <h2>8.3 Working Principle</h2>
  <p>
    When an administrator opens the application, the client verifies authentication status with Auth0. If unauthenticated, the user is redirected to Auth0 Universal Login or presents the institutional sign-in modal. Upon authentication, Auth0 returns verified user claims.
  </p>
  <p>
    The web client immediately initializes student records from local cache for instant display, then subscribes to Firebase Firestore using an <code>onSnapshot</code> listener. When an administrator creates, modifies, or deletes a student record, the client updates the UI optimistically, commits the change to Firestore, uploads the updated JSON dataset to Firebase Storage, dispatches the document to MongoDB Atlas via the Node.js REST API, and uploads a backup to Dropbox.
  </p>
</div>


<!-- ========================================== -->
<!-- PAGE 10: 9. SYSTEM DESIGN AND MODULES       -->
<!-- ========================================== -->
<div class="page">
  <h1>9. System Design and Modules</h1>
  <p>
    The application is organized into modular services according to the responsibilities of the integrated cloud providers.
  </p>

  <h2>9.1 Authentication & Identity Module</h2>
  <p>
    This module encapsulates user authentication using the <code>@auth0/auth0-spa-js</code> library and Firebase Auth. It manages user tokens, supports email/password login and Google OAuth single sign-on, and updates UI status badges upon successful authentication.
  </p>

  <h2>9.2 Student Record Management Module</h2>
  <p>
    This module implements full CRUD (Create, Read, Update, Delete) operations for student records. Each student record contains a Student ID, Full Name, Age, and Department. The module validates inputs, handles optimistic in-memory updates, and maintains consistent state across storage engines.
  </p>

  <h2>9.3 Multi-Engine & Hybrid Cloud Storage Module</h2>
  <p>
    This module provides a unified data access layer coordinating student persistence across multiple cloud storage engines. The storage engines are summarized below:
  </p>
  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Storage Option</th>
        <th style="width: 30%;">Technology & Model</th>
        <th style="width: 45%;">Characteristics</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>MongoDB Atlas</strong></td>
        <td>MongoDB Atlas (DBaaS)</td>
        <td>Managed NoSQL document persistence with BSON querying and secure server-side connection pooling.</td>
      </tr>
      <tr>
        <td><strong>Firestore</strong></td>
        <td>Google Cloud Firestore (BaaS)</td>
        <td>Serverless real-time document database with reactive <code>onSnapshot</code> stream listeners.</td>
      </tr>
      <tr>
        <td><strong>Firebase Storage</strong></td>
        <td>Google Cloud Storage (STaaS)</td>
        <td>Persistent cloud object storage bucket hosting <code>students.json</code> for global access.</td>
      </tr>
      <tr>
        <td><strong>Local Storage</strong></td>
        <td>Browser Web Storage API</td>
        <td>Zero-latency optimistic local cache ensuring the UI never hangs during network delays.</td>
      </tr>
    </tbody>
  </table>

  <h2>9.4 Dropbox Cloud Export and Backup Module</h2>
  <p>
    This module interfaces with the Dropbox Files API v2. It validates the user's Dropbox access token, checks account connection status via <code>/2/users/get_current_account</code>, serializes student records into formatted JSON, and uploads the dataset to <code>/students.json</code> using <code>mode=overwrite</code>.
  </p>
</div>


<!-- ========================================== -->
<!-- PAGE 11: 9.5 SEARCH & 9.6 API MODULE       -->
<!-- ========================================== -->
<div class="page">
  <h2>9.5 Search, Filter, and Analytics Dashboard Module</h2>
  <p>
    This module provides instant client-side filtering across student identifiers, full names, and academic departments. It dynamically computes real-time KPI metrics—Total Registered Students, Average Student Age, and Total Academic Departments—without requiring additional backend queries.
  </p>

  <h2>9.6 API and Error Handling Module</h2>
  <p>
    This module defines the RESTful endpoints used by the application, listed below. The backend processes requests and returns structured JSON responses. Robust error handling transforms low-level database and network errors into clear toast messages for administrators.
  </p>

  <h3>Node.js Backend Server (http://localhost:3000):</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 15%;">Method</th>
        <th style="width: 30%;">Endpoint</th>
        <th style="width: 25%;">Query / Body</th>
        <th style="width: 30%;">Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>GET</strong></td>
        <td><code>/api/mongodb/students</code></td>
        <td>None</td>
        <td>Fetches all student records from MongoDB Atlas cluster.</td>
      </tr>
      <tr>
        <td><strong>POST</strong></td>
        <td><code>/api/mongodb/student</code></td>
        <td>JSON student object</td>
        <td>Creates or updates a student record in MongoDB Atlas.</td>
      </tr>
      <tr>
        <td><strong>DELETE</strong></td>
        <td><code>/api/mongodb/student</code></td>
        <td><code>?id={studentId}</code></td>
        <td>Deletes a student record from MongoDB Atlas.</td>
      </tr>
      <tr>
        <td><strong>POST</strong></td>
        <td><code>/api/mongodb/sync</code></td>
        <td>JSON student array</td>
        <td>Synchronizes complete student roster into MongoDB Atlas.</td>
      </tr>
      <tr>
        <td><strong>POST</strong></td>
        <td><code>/api/mongodb/test</code></td>
        <td>None</td>
        <td>Tests connectivity and pings MongoDB Atlas cluster.</td>
      </tr>
    </tbody>
  </table>

  <h3>Dropbox Cloud Service (https://api.dropboxapi.com):</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 15%;">Method</th>
        <th style="width: 30%;">Endpoint</th>
        <th style="width: 25%;">Body</th>
        <th style="width: 30%;">Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>POST</strong></td>
        <td><code>/2/files/upload</code></td>
        <td>Binary stream of <code>students.json</code></td>
        <td>Uploads student roster backup to Dropbox.</td>
      </tr>
      <tr>
        <td><strong>POST</strong></td>
        <td><code>/2/users/get_current_account</code></td>
        <td>None (Authorization header)</td>
        <td>Validates Dropbox token and account connection.</td>
      </tr>
    </tbody>
  </table>
</div>


<!-- ========================================== -->
<!-- PAGE 12: 9.7 DATA FLOW & 9.8 DATA STRUCT   -->
<!-- ========================================== -->
<div class="page">
  <h2>9.7 Data Flow Diagram</h2>
  <div class="figure-container">
    <img class="figure-img" src="fig_dataflow.png" alt="Data Flow of StudentSphere">
    <div class="figure-caption">Figure 2: Data Flow Diagram of Authentication, Student Records Dispatch, and Multi-Cloud Sync.</div>
  </div>

  <h2>9.8 Data Structures</h2>
  <p>
    Each storage engine organizes student records according to its data model. MongoDB stores structured BSON documents, Firestore stores documents with real-time listeners, and Dropbox/Firebase Storage store full JSON arrays.
  </p>
  <div class="figure-container">
    <img class="figure-img" src="fig_datastructures.png" alt="Data Structures Used by Storage Engines">
    <div class="figure-caption">Figure 3: Data Structures Used Across Cloud Storage Engines.</div>
  </div>

  <p>An example student record serialized in <code>students.json</code> is shown below:</p>
  <pre>[
  {
    "id": "STU-101",
    "name": "Alex Morgan",
    "age": 21,
    "department": "Computer Science",
    "createdAt": "2026-10-19T10:30:00.000Z"
  }
]</pre>
</div>


<!-- ========================================== -->
<!-- PAGE 13: 10. IMPLEMENTATION & 10.1, 10.2   -->
<!-- ========================================== -->
<div class="page">
  <h1>10. Implementation</h1>
  <p>
    The frontend was implemented using pure HTML5, modern CSS3, and JavaScript ES modules. The backend was constructed with Node.js and Google Cloud Firebase Cloud Functions. Dependencies were managed via npm, and each service was configured to communicate with its respective cloud provider.
  </p>

  <h2>10.1 Backend and Frontend Setup</h2>
  <p>
    A Node.js project was initialized with ES module support (<code>"type": "module"</code>). The Node.js server (<code>server.js</code>) listens on port 3000, serving static web assets and defining REST endpoints at <code>/api/mongodb/*</code>. Firebase Hosting serves frontend assets in production and routes API requests to Cloud Functions.
  </p>

  <h2>10.2 Authentication Implementation</h2>
  <p>
    Auth0 was configured with tenant domain <code>dev-58o1wuwbx3qv1hfn.us.auth0.com</code>. The frontend initializes the Auth0 SPA SDK in <code>auth0-service.js</code>. Users can authenticate with email/password credentials or click <strong>"Continue with Google"</strong> to initiate Google OAuth federation:
  </p>
  <pre>const auth0Client = await createAuth0Client({
  domain: "dev-58o1wuwbx3qv1hfn.us.auth0.com",
  clientId: "YOUR_AUTH0_CLIENT_ID",
  authorizationParams: { redirect_uri: window.location.origin }
});</pre>

  <div class="figure-container">
    <img class="figure-img" style="max-height: 95mm;" src="fig_login.png" alt="Authentication Interface">
    <div class="figure-caption">Figure 4: StudentSphere Authentication Screen (Email/Password & Google SSO).</div>
  </div>
</div>


<!-- ========================================== -->
<!-- PAGE 14: 10.3 MONGO & 10.4 FIRESTORE       -->
<!-- ========================================== -->
<div class="page">
  <h2>10.3 MongoDB Atlas Integration</h2>
  <p>
    The Node.js backend connects to MongoDB Atlas using the official <code>mongodb</code> driver and a <code>mongodb+srv://</code> connection string. Connection pooling ensures high-throughput database interactions. Student documents contain <code>id</code>, <code>name</code>, <code>age</code>, and <code>department</code>. Free-tier M0 Atlas clusters can enter a paused state after inactivity, which must be resumed before database queries can execute.
  </p>

  <div class="figure-container">
    <img class="figure-img" style="max-height: 95mm;" src="fig_dashboard.png" alt="Main Dashboard Interface">
    <div class="figure-caption">Figure 5: Main Dashboard Displaying Real-Time Student Metrics and Department Roster.</div>
  </div>

  <h2>10.4 Firebase Cloud Firestore & Storage Integration</h2>
  <p>
    The Firebase Modular SDK (v10.12.0) is configured in <code>firebase-config.js</code>. The web client subscribes to student records using Firestore's <code>onSnapshot</code> listener, ensuring changes made on any terminal appear instantly:
  </p>
  <pre>const unsubscribe = onSnapshot(collection(db, "students"), (snapshot) => {
  const students = snapshot.docs.map(doc => doc.data());
  renderStudentTable(students);
  updateKPIs(students);
});</pre>
  <p>
    Concurrently, the complete roster is written to Google Firebase Storage bucket <code>website-82bc7.firebasestorage.app</code> as <code>students.json</code>.
  </p>
</div>


<!-- ========================================== -->
<!-- PAGE 15: 10.5 DROPBOX INTEGRATION          -->
<!-- ========================================== -->
<div class="page">
  <div class="figure-container">
    <img class="figure-img" style="max-height: 95mm;" src="fig_add_student.png" alt="Add Student Interface">
    <div class="figure-caption">Figure 6: Student Profile Creation Dialog with Field Validation.</div>
  </div>

  <h2>10.5 Dropbox API Integration</h2>
  <p>
    The Dropbox integration in <code>dropbox-service.js</code> communicates directly with the Dropbox Files API v2. A generated OAuth access token is passed in the Authorization header. When student records are updated, the entire student list is serialized as formatted JSON and uploaded to Dropbox:
  </p>
  <pre>const res = await fetch('https://content.dropboxapi.com/2/files/upload', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Dropbox-API-Arg': JSON.stringify({ path: '/students.json', mode: 'overwrite' }),
    'Content-Type': 'application/octet-stream'
  },
  body: new Blob([JSON.stringify(studentsList, null, 2)], { type: 'application/json' })
});</pre>
  <p>
    The service validates token permissions (<code>files.content.write</code> and <code>files.content.read</code>), ensuring reliable offsite backup.
  </p>
</div>


<!-- ========================================== -->
<!-- PAGE 16: 10.6 CLOUD MODELS & 11. SCREENSHOTS-->
<!-- ========================================== -->
<div class="page">
  <div class="figure-container">
    <img class="figure-img" style="max-height: 85mm;" src="fig_details.png" alt="Student Details Interface">
    <div class="figure-caption">Figure 7: Student Information and Academic Profile Modal.</div>
  </div>

  <h2>10.6 Cloud Service Models Used</h2>
  <p>StudentSphere leverages four primary cloud service models, each fulfilling a specialized role:</p>
  <table>
    <thead>
      <tr>
        <th style="width: 20%;">Cloud Service</th>
        <th style="width: 20%;">Provider</th>
        <th style="width: 18%;">Cloud Model</th>
        <th style="width: 42%;">Role in StudentSphere</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Auth0</strong></td>
        <td>Okta</td>
        <td><strong>IDaaS</strong></td>
        <td>Identity management, Universal Login, and Google OAuth SSO.</td>
      </tr>
      <tr>
        <td><strong>MongoDB Atlas</strong></td>
        <td>MongoDB Inc.</td>
        <td><strong>DBaaS</strong></td>
        <td>Managed NoSQL document database for structured records.</td>
      </tr>
      <tr>
        <td><strong>Firebase Firestore</strong></td>
        <td>Google Cloud</td>
        <td><strong>BaaS</strong></td>
        <td>Serverless real-time database with instant client stream listeners.</td>
      </tr>
      <tr>
        <td><strong>Firebase Storage</strong></td>
        <td>Google Cloud</td>
        <td><strong>STaaS</strong></td>
        <td>Cloud object storage bucket for persistent <code>students.json</code>.</td>
      </tr>
      <tr>
        <td><strong>Dropbox API</strong></td>
        <td>Dropbox</td>
        <td><strong>STaaS</strong></td>
        <td>Offsite file storage and automated JSON backup snapshots.</td>
      </tr>
    </tbody>
  </table>

  <h1>11. Application Screenshots and Results</h1>
  <p>This section documents the actual user interface and functionality of StudentSphere.</p>

  <h2>11.1 Authentication & Login Interface</h2>
  <p>
    Unauthenticated users are greeted by the authentication screen shown in Figure 4, supporting email/password authentication, registration, and Google OAuth sign-in.
  </p>
</div>


<!-- ========================================== -->
<!-- PAGE 17: 11.2 WORKSPACE & SEARCH           -->
<!-- ========================================== -->
<div class="page">
  <div class="figure-container">
    <img class="figure-img" style="max-height: 90mm;" src="fig_delete.png" alt="Delete Confirmation Modal">
    <div class="figure-caption">Figure 8: Record Deletion Safety Confirmation Dialog.</div>
  </div>

  <h2>11.2 Main Student Dashboard & Metrics</h2>
  <p>
    Upon successful login, administrators access the primary dashboard (Figure 5) showing live KPI counters (Total Students, Average Student Age, Total Departments) and the interactive student directory table.
  </p>

  <div class="figure-container">
    <img class="figure-img" style="max-height: 90mm;" src="fig_search.png" alt="Live Search Interface">
    <div class="figure-caption">Figure 9: Real-Time Search and Department Filtering Interface.</div>
  </div>

  <h2>11.3 Search and Department Filter Operations</h2>
  <p>
    The search input filters student records in real time across Student ID, Full Name, and Department. Selecting a department from the dropdown isolates the corresponding roster immediately, as shown in Figure 9.
  </p>
</div>


<!-- ========================================== -->
<!-- PAGE 18: 11.4 CLOUD SETTINGS SCREENSHOTS   -->
<!-- ========================================== -->
<div class="page">
  <div class="figure-container">
    <img class="figure-img" style="max-height: 95mm;" src="fig_settings_dropbox.png" alt="Dropbox Settings">
    <div class="figure-caption">Figure 10: Dropbox Cloud Storage Integration and Token Management.</div>
  </div>

  <h2>11.4 Dropbox Cloud Storage Synchronization</h2>
  <p>
    The system settings modal includes a dedicated Dropbox tab (Figure 10). Administrators can paste an OAuth access token, verify connection to the Dropbox account, and trigger automated JSON backup uploads to <code>/students.json</code>.
  </p>

  <h2>11.5 Student Information View and Deletion</h2>
  <p>
    Clicking <strong>"Details"</strong> on any student row opens the student inspection modal (Figure 7), while clicking <strong>"Delete"</strong> opens the safety confirmation dialog (Figure 8) to prevent accidental record removal.
  </p>
</div>


<!-- ========================================== -->
<!-- PAGE 19: 11.6 MONGO SETTINGS & 12. TESTING -->
<!-- ========================================== -->
<div class="page">
  <div class="figure-container">
    <img class="figure-img" style="max-height: 95mm;" src="fig_settings_mongo.png" alt="MongoDB Atlas Settings">
    <div class="figure-caption">Figure 11: MongoDB Atlas Cloud Database Configuration and Health Diagnostics.</div>
  </div>

  <h2>11.6 MongoDB Atlas Database Configuration</h2>
  <p>
    The MongoDB Atlas configuration tab (Figure 11) allows administrators to verify cluster connectivity, view database and collection names, and trigger bulk synchronization of student records from the browser to the Atlas cluster.
  </p>

  <h1>12. Testing and Results</h1>
  <p>
    Testing was conducted to verify application features, authentication flows, database persistence, and multi-cloud synchronization.
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 32%;">Test Case</th>
        <th style="width: 38%;">Expected Result</th>
        <th style="width: 30%;">Actual Result</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Start Node.js application server</td>
        <td>Server starts on port 3000 without errors</td>
        <td>Server running at http://localhost:3000</td>
      </tr>
      <tr>
        <td>Sign in with email and password</td>
        <td>User is authenticated and redirected to dashboard</td>
        <td>Authentication successful; dashboard displayed</td>
      </tr>
      <tr>
        <td>Sign in with Google OAuth (Auth0)</td>
        <td>Redirects to Google login and returns valid token</td>
        <td>Google sign-in completed; session active</td>
      </tr>
    </tbody>
  </table>
</div>


<!-- ========================================== -->
<!-- PAGE 20: 12. TESTING MATRIX CONT.          -->
<!-- ========================================== -->
<div class="page">
  <table>
    <thead>
      <tr>
        <th style="width: 32%;">Test Case</th>
        <th style="width: 38%;">Expected Result</th>
        <th style="width: 30%;">Actual Result</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Real-time KPI calculation</td>
        <td>KPI cards calculate total students, average age, and department count accurately</td>
        <td>Calculated correctly: 5 students, 21 yrs avg age, 5 departments</td>
      </tr>
      <tr>
        <td>Create new student record</td>
        <td>Student record is saved and rendered in the table immediately</td>
        <td>Student record created; rendered via optimistic update</td>
      </tr>
      <tr>
        <td>Firestore real-time synchronization</td>
        <td>Records updated in one tab appear instantly in another</td>
        <td>Firestore onSnapshot updated secondary client immediately</td>
      </tr>
      <tr>
        <td>Upload to Firebase Cloud Storage</td>
        <td>JSON array is uploaded to bucket website-82bc7.firebasestorage.app</td>
        <td>File students.json updated in Cloud Storage bucket</td>
      </tr>
      <tr>
        <td>Live search by student name/ID</td>
        <td>Table filters matching student records dynamically</td>
        <td>Query 'Data' isolated Data Science student STU-102</td>
      </tr>
      <tr>
        <td>Filter by academic department</td>
        <td>Table displays only students belonging to selected department</td>
        <td>Dropdown selected 'Computer Science'; filtered accurately</td>
      </tr>
      <tr>
        <td>View student details</td>
        <td>Modal opens displaying complete student profile attributes</td>
        <td>Modal opened with ID, name, age, and department</td>
      </tr>
      <tr>
        <td>Delete student record</td>
        <td>Safety modal prompts confirmation; record is removed on confirm</td>
        <td>Record deleted and removed from UI and cloud stores</td>
      </tr>
      <tr>
        <td>MongoDB Atlas connection test</td>
        <td>POST /api/mongodb/test verifies connectivity to Atlas</td>
        <td>Connection ping successful: { success: true }</td>
      </tr>
      <tr>
        <td>MongoDB Atlas batch sync</td>
        <td>POST /api/mongodb/sync writes complete student roster to Atlas</td>
        <td>All student documents synced into studentsphere_db</td>
      </tr>
      <tr>
        <td>Dropbox cloud file backup</td>
        <td>Student JSON is uploaded to /students.json in Dropbox</td>
        <td>File uploaded to Dropbox account successfully</td>
      </tr>
      <tr>
        <td>Invalid Dropbox token handling</td>
        <td>System catches 401 error and displays friendly toast notification</td>
        <td>Toast displayed: 'Invalid or expired Dropbox token'</td>
      </tr>
    </tbody>
  </table>
</div>


<!-- ========================================== -->
<!-- PAGE 21: 12.1-12.5 & 13. ADVANTAGES        -->
<!-- ========================================== -->
<div class="page">
  <h2>12.1 Functional Testing</h2>
  <p>
    Functional testing confirmed that all primary features—student creation, details viewing, deletion prompts, live search, and department filtering—perform reliably according to specifications.
  </p>

  <h2>12.2 Authentication Testing</h2>
  <p>
    Authentication testing verified that protected actions require valid session tokens, and that unauthenticated users cannot view or manipulate student records.
  </p>

  <h2>12.3 Database Testing</h2>
  <p>
    Database testing verified that student documents are correctly created, updated, and deleted in MongoDB Atlas and Google Cloud Firestore. Firestore listeners updated client interfaces without manual refreshes.
  </p>

  <h2>12.4 File Storage & Cloud Export Testing</h2>
  <p>
    File export testing verified that valid JSON files are generated and uploaded to Google Firebase Storage and Dropbox with correct syntax and write permissions.
  </p>

  <h2>12.5 Result Discussion</h2>
  <p>
    The application demonstrates how authentication, multi-cloud databases, and cloud file storage can be integrated through a single web portal. During testing, it was noted that MongoDB Atlas free-tier clusters can enter a paused state after inactivity, requiring resumption before SRV connections succeed. Optimistic UI caching ensured that temporary cloud latency never froze the user interface.
  </p>

  <h1>13. Advantages</h1>
  <ol>
    <li><strong>Centralized Access:</strong> A unified administrative workspace for creating, searching, and managing student profiles.</li>
    <li><strong>Multi-Cloud Resilience:</strong> Combining Auth0, MongoDB Atlas, Firebase, and Dropbox eliminates single-vendor lock-in.</li>
    <li><strong>Zero-Latency UI:</strong> Optimistic caching renders user actions in under 50 milliseconds while background sync occurs asynchronously.</li>
    <li><strong>Real-Time Updates:</strong> Firestore listeners update connected clients instantaneously without polling.</li>
    <li><strong>Enterprise Authentication:</strong> Auth0 provides secure identity management, ensuring user credentials never touch local servers.</li>
    <li><strong>Automated Offsite Backup:</strong> Student rosters are backed up to Dropbox as standardized JSON files for disaster recovery.</li>
    <li><strong>Decoupled Architecture:</strong> Frontend and backend services operate independently, simplifying maintenance.</li>
    <li><strong>Extensibility:</strong> Additional student attributes, academic grades, and course modules can be added easily.</li>
  </ol>
</div>


<!-- ========================================== -->
<!-- PAGE 22: 14. LIMITATIONS & 15. FUTURE      -->
<!-- ========================================== -->
<div class="page">
  <h1>14. Limitations</h1>
  <ul>
    <li>The application depends on internet connectivity for cloud database synchronization.</li>
    <li>Cloud service access depends on valid API tokens, permissions, and network whitelists.</li>
    <li>Free-tier MongoDB Atlas clusters can pause after periods of inactivity and must be resumed before use.</li>
    <li>Dropbox access tokens must be regenerated or refreshed periodically.</li>
    <li>Dropbox synchronization currently pushes files outward but does not parse manual external edits back into the database.</li>
    <li>Cloud service usage is subject to free-tier storage and API call quotas.</li>
    <li>The current implementation focuses on administrative access rather than differentiated multi-tier student/faculty roles.</li>
    <li>The local development proxy setup runs locally and is not automatically accessible over the public internet without hosting deployment.</li>
  </ul>

  <h1>15. Future Enhancements</h1>
  <ol>
    <li>Implement Role-Based Access Control (RBAC) distinguishing between Student, Faculty, and Admin roles.</li>
    <li>Add course enrollment tracking, credit hours, and faculty advisor assignments.</li>
    <li>Provide one-click export of student rosters to Microsoft Excel (.xlsx) and CSV formats.</li>
    <li>Integrate academic grading scales with automated GPA and CGPA computation.</li>
    <li>Add student photo upload and identification card storage via Firebase Cloud Storage.</li>
    <li>Implement bi-directional Dropbox synchronization using webhook notifications.</li>
    <li>Integrate SMS and email notification services (e.g., Twilio / SendGrid) for institutional announcements.</li>
    <li>Develop a self-service student portal where students can log in to view their personal academic records.</li>
    <li>Add dynamic dark/light theme switching with saved user preferences.</li>
    <li>Package backend services into Docker containers and deploy to Google Cloud Run.</li>
    <li>Add automated unit and end-to-end testing with GitHub Actions CI/CD pipelines.</li>
    <li>Implement comprehensive audit logging to track all administrative record modifications.</li>
  </ol>
  <p class="italic-note">These are proposed improvements and are not described as completed features.</p>

  <h1>16. Conclusion</h1>
  <p>
    StudentSphere was developed as a cloud computing project to demonstrate the practical integration of identity, database, backend, and storage services in a single academic application.
  </p>
</div>


<!-- ========================================== -->
<!-- PAGE 23: CONCLUSION CONT. & 17. REFERENCES -->
<!-- ========================================== -->
<div class="page">
  <p>
    HTML5 and CSS3 provide an intuitive, responsive user interface, while Node.js and Google Cloud Functions handle backend routing. Auth0 is used for authentication and Google single sign-on, MongoDB Atlas and Firebase Firestore store student records, and Firebase Storage and the Dropbox API store persistent JSON datasets. Together, they demonstrate the IDaaS, DBaaS, BaaS, and STaaS cloud service models.
  </p>
  <p>
    The project provides practical knowledge of full-stack web development, serverless microservices, token-based authentication, NoSQL database operations, real-time client synchronization, environment configuration, and cloud storage integration.
  </p>
  <p>
    The implementation can be extended with features such as course enrollment, GPA calculation, Excel exports, and containerized cloud deployment. Overall, the project provides a practical demonstration of cloud computing concepts through a multi-cloud student records and information management platform.
  </p>

  <h1>17. References</h1>
  <ol>
    <li>Auth0 Documentation. https://auth0.com/docs</li>
    <li>Google Cloud Firebase Documentation. https://firebase.google.com/docs</li>
    <li>Firebase Cloud Firestore Documentation. https://firebase.google.com/docs/firestore</li>
    <li>Firebase Cloud Storage Documentation. https://firebase.google.com/docs/storage</li>
    <li>Firebase Admin SDK Documentation. https://firebase.google.com/docs/admin/setup</li>
    <li>Node.js Official Documentation. https://nodejs.org/docs/latest/api/</li>
    <li>MongoDB Atlas Documentation. https://www.mongodb.com/docs/atlas/</li>
    <li>MongoDB Node.js Driver Documentation. https://www.mongodb.com/docs/drivers/node/current/</li>
    <li>Dropbox API Documentation. https://www.dropbox.com/developers/documentation/http/overview</li>
    <li>npm Documentation. https://docs.npmjs.com/</li>
    <li>MDN Web Docs: Modern JavaScript & Fetch API. https://developer.mozilla.org/</li>
    <li>RFC 6749: The OAuth 2.0 Authorization Framework. https://datatracker.ietf.org/doc/html/rfc6749</li>
  </ol>
</div>

</body>
</html>
"""

html_path = os.path.join(WORKSPACE, "StudentSphere_Project_Report.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML Report generated at: {html_path}")

# Compile HTML to PDF using Chrome Headless
pdf_path = os.path.join(WORKSPACE, "StudentSphere_Project_Report.pdf")
print("Rendering PDF with headless Chrome...")
res = subprocess.run([
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--no-sandbox",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    f"file:///{html_path.replace(os.sep, '/')}"
], capture_output=True, text=True)

if os.path.exists(pdf_path):
    size_bytes = os.path.getsize(pdf_path)
    print(f"PDF successfully generated at: {pdf_path} (Size: {size_bytes} bytes)")
else:
    print(f"PDF generation failed: {res.stderr}")
