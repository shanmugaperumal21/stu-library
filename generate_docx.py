# -*- coding: utf-8 -*-
"""
Generate Microsoft Word (.docx) Academic Report for StudentSphere
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

WORKSPACE = r"e:\st-20261015T083357Z-1-001"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_docx():
    doc = docx.Document()

    # Set page margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69) # A4

    # Configure default Normal style
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x11, 0x11, 0x11)

    # ---------------------------------------------------------
    # COVER PAGE
    # ---------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(40)
    p_title.paragraph_format.space_after = Pt(10)
    run_title = p_title.add_run("STUDENTSPHERE\n")
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(20)
    run_sub = p_sub.add_run("A Multi-Cloud Student Management and Academic Records Platform\n")
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_after = Pt(4)
    run_rep = p_rep.add_run("CLOUD COMPUTING LABORATORY PROJECT REPORT\n(22IT580)")
    run_rep.font.size = Pt(12)
    run_rep.font.bold = True

    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subm.paragraph_format.space_before = Pt(35)
    p_subm.paragraph_format.space_after = Pt(15)
    run_subm = p_subm.add_run("Submitted by")
    run_subm.font.italic = True
    run_subm.font.size = Pt(12)

    team_members = [
        ("SHANMUGA PERUMAL A", "2403917720521313"),
        ("VANAMAMALAI M", "2403917720521086"),
        ("EDWIN MOSES G", "2403917720521305")
    ]

    for name, reg in team_members:
        p_mem = doc.add_paragraph()
        p_mem.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_mem.paragraph_format.space_after = Pt(4)
        run_name = p_mem.add_run(f"{name} — ")
        run_name.font.bold = True
        run_name.font.size = Pt(11.5)
        run_reg = p_mem.add_run(f"Register Number: {reg}")
        run_reg.font.size = Pt(11)

    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.space_before = Pt(65)
    p_bot.paragraph_format.space_after = Pt(4)
    run_bot1 = p_bot.add_run("Submitted in partial fulfilment of the requirements for the Cloud Computing Laboratory\n\n")
    run_bot1.font.size = Pt(10.5)

    run_dept = p_bot.add_run("Department of Information Technology\n")
    run_dept.font.bold = True
    run_dept.font.size = Pt(12)

    run_col = p_bot.add_run("Thiagarajar College of Engineering, Madurai\n")
    run_col.font.size = Pt(11.5)

    run_yr = p_bot.add_run("Academic Year: 2026–2027")
    run_yr.font.size = Pt(11)

    doc.add_page_break()

    # ---------------------------------------------------------
    # ABSTRACT & TABLE OF CONTENTS
    # ---------------------------------------------------------
    def add_h1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.bold = True
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        return h

    def add_h2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        return h

    def add_h3(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.bold = True
        r.font.size = Pt(11)
        return h

    def add_p(text, justify=True):
        p = doc.add_paragraph()
        if justify:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.18
        r = p.add_run(text)
        r.font.size = Pt(11)
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.size = Pt(11)
        return p

    def add_num(num_str, text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(f"{num_str} ")
        r1.font.bold = True
        r1.font.size = Pt(11)
        r2 = p.add_run(text)
        r2.font.size = Pt(11)
        return p

    def add_image_figure(fig_name, caption):
        img_path = os.path.join(WORKSPACE, fig_name)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(3)
            doc.add_picture(img_path, width=Inches(5.8))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(10)
            r_cap = p_cap.add_run(caption)
            r_cap.font.italic = True
            r_cap.font.size = Pt(9.5)
            r_cap.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    add_h1("Abstract")
    add_p("StudentSphere is a full-stack, cloud-native student information and directory management platform developed to let academic institutions and faculty administrators store, organize, search, filter, and backup student records across hybrid multi-cloud environments. The application demonstrates how several cloud service models can be harmoniously combined in a single institutional platform: Identity as a Service (IDaaS), Database as a Service (DBaaS), Backend as a Service (BaaS), and Storage as a Service (STaaS).")
    add_p("The frontend is an intuitive Single Page Application (SPA) built with HTML5, vanilla CSS3 featuring modern glassmorphic aesthetics, and JavaScript ES modules. It communicates with an extensible Node.js HTTP backend server and Google Cloud Firebase Cloud Functions. Auth0 is employed for Identity as a Service (IDaaS) with Universal Login and Google OAuth 2.0 federation. MongoDB Atlas provides managed Database as a Service (DBaaS) for structured document persistence, while Google Firebase Cloud Firestore serves as Backend as a Service (BaaS) providing real-time data synchronization. Firebase Cloud Storage and the Dropbox API v2 supply Storage as a Service (STaaS) for instant cloud object persistence and automated JSON cloud backup.")
    add_p("Administrators can create, view, search, and delete student records, filter the roster by academic department, inspect detailed demographic attributes, and initiate one-click synchronization to Dropbox cloud storage and MongoDB Atlas. Authentication middleware and token validation ensure that only authorized administrative users can access and modify student records.")
    add_p("The main objective of the project is to demonstrate the practical integration of multiple independent cloud platforms, each chosen for a specific responsibility, rather than relying on a single vendor or a vulnerable local desktop system. The project provides hands-on experience in REST API development, serverless microservice design, token-based authentication, NoSQL document databases, real-time data streaming, and automated cloud file synchronization.")
    
    p_kw = add_p("")
    r_kw_label = p_kw.add_run("Keywords: ")
    r_kw_label.font.bold = True
    p_kw.add_run("Cloud Computing, StudentSphere, Multi-Cloud Integration, Auth0, MongoDB Atlas, Firebase Firestore, Firebase Storage, Dropbox API, IDaaS, DBaaS, BaaS, STaaS, Node.js.")

    add_h1("Table of Contents")
    toc_items = [
        "1. Introduction", "2. Problem Statement", "3. Objectives",
        "4. Existing System", "5. Proposed System", "6. System Requirements",
        "7. Technologies Used", "8. System Architecture", "9. System Design and Modules",
        "10. Implementation", "11. Application Screenshots and Results", "12. Testing and Results",
        "13. Advantages", "14. Limitations", "15. Future Enhancements",
        "16. Conclusion", "17. References"
    ]
    for item in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.left_indent = Inches(0.2)
        r = p_t.add_run(item)
        r.font.size = Pt(11)

    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(6)
    p_note.paragraph_format.space_after = Pt(12)
    r_n = p_note.add_run("Note: update the page numbers after the final formatting.")
    r_n.font.italic = True
    r_n.font.size = Pt(10)

    doc.add_page_break()

    # ---------------------------------------------------------
    # 1. INTRODUCTION
    # ---------------------------------------------------------
    add_h1("1. Introduction")
    add_p("Cloud computing is a technology that provides computing resources such as storage, databases, servers, identity services, and software through the internet. It allows applications to use these resources on demand without maintaining all the required infrastructure locally.")
    add_p("Academic institutions, universities, and departmental offices regularly maintain large volumes of student records, including Student IDs, full names, age demographics, and department affiliations. Traditionally, these records are scattered across localized spreadsheets, personal office computers, disparate flat files, or single-vendor proprietary systems, making them difficult to locate, share securely, and backup against hardware failure.")
    add_p("StudentSphere is designed to provide a centralized, secure platform for managing student records through modern cloud services. It combines enterprise identity federation, multiple database backends, and cloud file storage in one application, ensuring that institutional data is always accessible, resilient, and synchronized across departments.")
    add_p("The application follows a decoupled, multi-tier architecture. A modern Single Page Application provides the user interface. A Node.js HTTP server handles REST API endpoints and static file serving, while Google Cloud Firebase Cloud Functions execute serverless database operations with Secret Manager credential protection.")
    add_p("Auth0 is responsible for user identity and authentication. MongoDB Atlas and Firebase Firestore store structured student records. Dropbox API v2 and Firebase Cloud Storage provide cloud object storage in which student rosters are saved as persistent JSON datasets.")
    add_p("The integration of these services demonstrates how multiple cloud platforms can work together in a practical application. The project also introduces vital cloud concepts such as OAuth 2.0 and OpenID Connect, JSON Web Tokens (JWT), managed NoSQL clusters, real-time WebSocket listeners, and multi-cloud disaster recovery.")

    add_h2("1.1 Need for the Project")
    add_p("Academic administrators and faculty members need fast, secure access to student records from any device. The need for the project includes:")
    add_bullet("Providing authenticated, institutional access to centralized student databases.")
    add_bullet("Storing student records in managed cloud databases instead of volatile local files.")
    add_bullet("Eliminating single-vendor lock-in by distributing workloads across independent cloud providers.")
    add_bullet("Providing instant live search and department-level filtering across all student records.")
    add_bullet("Automating offsite cloud backups to personal or institutional Dropbox storage.")
    add_bullet("Demonstrating the simultaneous integration of IDaaS, DBaaS, BaaS, and STaaS in a single academic portal.")

    add_h2("1.2 Scope of the Project")
    add_p("The scope of StudentSphere includes secure administrative authentication, student record creation, retrieval, viewing, updating, and deletion (CRUD), multi-cloud storage synchronization through Firestore and MongoDB Atlas, and automated cloud file export to Dropbox and Firebase Cloud Storage. The application is intended as an academic implementation and demonstration of cloud computing paradigms.")

    # ---------------------------------------------------------
    # 2. PROBLEM STATEMENT & 3. OBJECTIVES
    # ---------------------------------------------------------
    add_h1("2. Problem Statement")
    add_p("Educational institutions keep student records in many disparate locations, including desktop spreadsheet applications, local text files, and isolated office workstations. When student details are stored separately across faculty desks, searching for records, updating student details, and aggregating departmental rosters becomes inconvenient, slow, and prone to data discrepancies.")
    add_p("Local storage also severely limits access when faculty members work from different terminals, lecture halls, or remote locations. Furthermore, relying on a single storage backend creates critical vendor lock-in; a service disruption from that provider completely halts institutional operations. Managing user access safely, preserving data privacy, and generating usable data backups typically requires extensive manual effort and third-party software.")
    add_p("Therefore, a cloud-based student management platform is needed that combines secure authentication, flexible multi-database storage, real-time synchronization, and automated cloud file export in one cohesive application. StudentSphere solves this challenge by integrating Auth0, MongoDB Atlas, Firebase Cloud Firestore, Firebase Storage, and Dropbox through an intuitive web client, a Node.js REST server, and serverless Cloud Functions.")

    add_h1("3. Objectives")
    add_p("The primary objective is to develop a cloud-native application that demonstrates the practical integration of multiple cloud service models. The specific objectives are:")
    add_num("1.", "To develop a responsive Single Page Application using HTML5, modern CSS3 with glassmorphism styling, and vanilla JavaScript ES modules.")
    add_num("2.", "To develop a backend REST API using Node.js for MongoDB Atlas integration and static asset serving.")
    add_num("3.", "To implement user authentication and Google Single Sign-On using Auth0 Identity Platform.")
    add_num("4.", "To store student documents in MongoDB Atlas as a managed cloud database (DBaaS).")
    add_num("5.", "To use Firebase Cloud Firestore for real-time reactive synchronization of student records across connected clients.")
    add_num("6.", "To provide persistent object storage in Firebase Cloud Storage as students.json.")
    add_num("7.", "To integrate the Dropbox API v2 for offsite cloud backup and disaster recovery.")
    add_num("8.", "To provide resilient optimistic UI updates backed by browser local storage caching.")
    add_num("9.", "To test and evaluate the communication and fault tolerance between the application and external cloud services.")

    add_h2("3.1 Project Outcomes")
    add_bullet("An interactive administrative portal for creating, viewing, searching, and deleting student profiles.")
    add_bullet("Authentication-based access control protecting student records from unauthorized access.")
    add_bullet("Real-time data streaming where database updates reflect immediately on all client screens without refreshing.")
    add_bullet("Hybrid data persistence across MongoDB Atlas, Firebase Firestore, and Firebase Cloud Storage.")
    add_bullet("Direct-to-cloud automated backup snapshots into Dropbox as /students.json.")

    # ---------------------------------------------------------
    # 4. EXISTING & 5. PROPOSED SYSTEM
    # ---------------------------------------------------------
    add_h1("4. Existing System")
    add_p("In a traditional institutional setup, departments manage student records using localized spreadsheet files (e.g., Microsoft Excel), local CSV/JSON files, or on-premise desktop database management systems (such as local MS Access or standalone MySQL instances). Each department maintains its own files independently, requiring administrative personnel to manually reconcile rosters, email copies between offices, and manage their own local backups.")

    add_h2("4.1 Disadvantages of the Existing System")
    add_bullet("Student records are scattered across multiple office workstations and departmental folders.")
    add_bullet("Access is strictly dependent on the physical device where the files are stored.")
    add_bullet("Searching across student IDs, names, and departments is cumbersome across multiple files.")
    add_bullet("User access control, password security, and student data confidentiality are difficult to enforce.")
    add_bullet("A single storage provider or hard drive failure causes catastrophic and permanent data loss.")
    add_bullet("Exporting student rosters to cloud storage is a tedious, manual process prone to human error.")
    add_bullet("Integrating multiple independent cloud services manually requires significant engineering overhead.")

    add_h1("5. Proposed System")
    add_p("The proposed StudentSphere system provides a centralized web application that seamlessly unites authentication, real-time database, managed cloud cluster, and distributed cloud file storage services into a cohesive portal.")
    add_p("Auth0 manages identity authentication and token issuance through OpenID Connect and Google OAuth federation. The web client communicates directly with Google Firebase Cloud Firestore via real-time reactive listeners (onSnapshot), ensuring that updates appear instantly on all active screens without manual browser refreshes. Concurrently, records are persisted into Google Firebase Cloud Storage as students.json.")
    add_p("For structured database persistence, the application routes data through a Node.js REST API to MongoDB Atlas (DBaaS). An integrated Dropbox module interfaces directly with Dropbox Files API v2 to save student rosters as standalone cloud backup files.")

    add_h2("5.1 Advantages of the Proposed System")
    add_bullet("Centralized administrative portal accessible from any desktop or mobile web browser.")
    add_bullet("Authentication-based access control and secure token validation.")
    add_bullet("Zero UI latency through optimistic client-side caching.")
    add_bullet("Real-time, reactive roster updates across all active sessions without manual polling.")
    add_bullet("Automated export and offsite cloud backup of student records to Dropbox.")
    add_bullet("Multi-cloud resilience that eliminates vendor lock-in by utilizing Google Cloud, MongoDB Atlas, and Dropbox in parallel.")
    add_bullet("Decoupled, modular architecture supporting independent scaling and straightforward maintenance.")

    add_h2("5.2 Comparison")
    table_comp = doc.add_table(rows=7, cols=2)
    set_table_borders(table_comp)
    table_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_headers = ["Existing Approach", "Proposed StudentSphere Approach"]
    for c_idx, h_text in enumerate(comp_headers):
        cell = table_comp.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_background(cell, "F1F5F9")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)

    comp_data = [
        ("Student records are stored in local spreadsheet files or on-premise desktops.", "Records are stored simultaneously across MongoDB Atlas, Firestore, and Cloud Storage."),
        ("Only one local storage location is used, risking complete data loss.", "Multi-cloud hybrid storage ensures continuous redundancy and disaster recovery."),
        ("Separate, unencrypted passwords or shared credentials must be maintained.", "Enterprise IDaaS via Auth0 is integrated for Universal Login and Google SSO."),
        ("Changes require manual refreshing, emailing files, or periodic re-importing.", "Firebase Firestore real-time listeners update the interface instantaneously."),
        ("Files are backed up manually to USB flash drives or external drives.", "Student datasets are automatically synchronized to Dropbox as /students.json."),
        ("Cloud services operate in silos or are not utilized at all.", "Four cloud service models (IDaaS, DBaaS, BaaS, STaaS) operate in harmony.")
    ]
    for r_idx, (c1, c2) in enumerate(comp_data):
        row = table_comp.rows[r_idx + 1]
        row.cells[0].text = c1
        row.cells[1].text = c2
        for cell in row.cells:
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # ---------------------------------------------------------
    # 6. SYSTEM REQUIREMENTS & 7. TECHNOLOGIES USED
    # ---------------------------------------------------------
    add_h1("6. System Requirements")
    add_p("The application requires a computer capable of executing Node.js and a modern browser with internet connectivity. Cloud accounts must be configured with active credentials before corresponding functions operate.")

    add_h2("6.1 Hardware Requirements")
    add_bullet("Computer or laptop (Intel Core i3 / AMD Ryzen 3 or higher).")
    add_bullet("Minimum 4 GB RAM recommended (8 GB preferred).")
    add_bullet("Sufficient disk space for Node.js modules and dependencies (at least 500 MB free).")
    add_bullet("Active internet connection (minimum 1 Mbps).")
    add_bullet("Keyboard, pointing device, and display monitor (1080p resolution recommended).")

    add_h2("6.2 Software Requirements")
    add_bullet("Operating System: Windows 10/11, macOS, or Linux.")
    add_bullet("Runtime Environment: Node.js (v18.x, v20.x, or v22.x LTS).")
    add_bullet("Package Manager: npm (v9.x or higher).")
    add_bullet("Frontend Technologies: HTML5, CSS3 with glassmorphism styling, and JavaScript ES Modules.")
    add_bullet("Backend Server: Node.js native HTTP server and Firebase Cloud Functions (2nd Gen).")
    add_bullet("Authentication Service: Auth0 by Okta.")
    add_bullet("Database Services: MongoDB Atlas (M0 Free Tier) and Google Cloud Firestore.")
    add_bullet("Cloud Storage Services: Google Firebase Storage and Dropbox API v2.")
    add_bullet("Development Tools: Visual Studio Code, Git CLI, and modern web browser (Chrome or Edge).")

    add_h2("6.3 Functional Requirements")
    add_num("1.", "Authenticate users securely through Auth0 (institutional email/password or Google SSO).")
    add_num("2.", "Validate identity claims and maintain persistent authenticated user sessions.")
    add_num("3.", "Create student records with unique Student ID, Full Name, Age, and Department.")
    add_num("4.", "Display student records in an interactive, responsive data table with status indicators.")
    add_num("5.", "Update student records and render modifications immediately across all clients.")
    add_num("6.", "Delete student records from selected cloud storage engines with safety confirmation.")
    add_num("7.", "Provide real-time multi-field search across Student ID, Name, and Department.")
    add_num("8.", "Filter student rosters dynamically by selecting specific academic departments.")
    add_num("9.", "Synchronize student datasets to Google Firebase Storage as students.json.")
    add_num("10.", "Export and backup student records to personal Dropbox accounts via Dropbox API v2.")
    add_num("11.", "Report cloud service connection statuses and diagnostics through the system settings modal.")

    add_h2("6.4 Non-Functional Requirements")
    add_bullet("Security: Protected administrative operations require valid authentication; sensitive database connection strings are stored server-side in Secret Manager.")
    add_bullet("Reliability: Multi-engine architecture ensures that failure in one cloud service does not prevent access through secondary engines.")
    add_bullet("Usability: The interface provides intuitive live search, color-coded department tags, clear visual hierarchy, and non-blocking toast notifications.")
    add_bullet("Maintainability: The frontend SPA, Node.js API server, and Cloud Functions are decoupled into modular ES modules.")
    add_bullet("Performance: Initial page load completes in under 1.5 seconds; local optimistic updates render in under 50 milliseconds.")

    add_h1("7. Technologies Used")
    add_h2("7.1 Frontend Architecture (HTML5, Vanilla CSS, ES Modules)")
    add_p("The frontend is constructed using pure HTML5, modern CSS3, and JavaScript ES modules. By avoiding heavy UI framework dependencies, the application achieves lightning-fast load times. The interface is styled with custom modern CSS utilizing CSS Custom Properties, backdrop-filter glassmorphism, flexbox and grid layouts, and smooth micro-animations.")

    add_h2("7.2 Node.js HTTP Runtime and Firebase Cloud Functions")
    add_p("Node.js is used to execute server-side JavaScript outside the browser. A native Node.js HTTP server (server.js) on port 3000 handles static asset delivery and REST endpoints at /api/mongodb/*. In cloud deployments, Google Firebase Cloud Functions (2nd Gen) provide serverless REST endpoints with Secret Manager integration.")

    add_h2("7.3 Auth0 Identity Platform")
    add_p("Auth0, by Okta, is an enterprise identity platform that handles user registration, login, session token issuance, and social OAuth federation. In StudentSphere, the frontend uses the @auth0/auth0-spa-js library and Universal Login based on OpenID Connect (OIDC). Users authenticate with institutional email credentials or through Google Single Sign-On (google-oauth2 connection).")

    add_h2("7.4 Google Firebase Cloud Firestore")
    add_p("Firebase Cloud Firestore is a serverless NoSQL document database featuring real-time data synchronization. The web client uses the Firebase modular SDK (v10.12.0) and onSnapshot listeners to subscribe to the students collection, updating the UI instantly whenever records are added, modified, or removed.")

    add_h2("7.5 Google Firebase Cloud Storage")
    add_p("Firebase Cloud Storage is an enterprise object storage service backed by Google Cloud Storage. In StudentSphere, the complete student roster is serialized and stored in bucket website-82bc7.firebasestorage.app as a persistent students.json file.")

    add_h2("7.6 MongoDB Atlas")
    add_p("MongoDB Atlas is a fully managed cloud NoSQL document database. The Node.js backend connects to MongoDB Atlas using the official mongodb driver (v7.7.0) via a mongodb+srv:// connection string with DNS SRV record discovery. Records are stored as structured documents in database studentsphere_db under collection students.")

    add_h2("7.7 Dropbox API v2")
    add_p("Dropbox provides cloud file storage and an HTTP REST API for file operations. StudentSphere interfaces directly with Dropbox Files API v2 endpoints (/2/files/upload and /2/users/get_current_account) using OAuth 2.0 bearer tokens to save student backups to /students.json.")

    add_h2("7.8 npm and Package Ecosystem")
    add_p("npm manages backend dependencies such as the official mongodb driver and firebase-admin. npm scripts allow starting the local development server with environment variables loaded automatically.")

    add_h2("7.9 Environment Variables and Configuration Security")
    add_p("Environment variables store sensitive configuration values such as server ports, Auth0 credentials, Firebase configuration keys, and the MongoDB connection URI. Sensitive credentials are kept in a private .env file locally and stored in Google Secret Manager for production deployments, ensuring they are never exposed in public repositories or screenshots.")

    doc.add_page_break()

    # ---------------------------------------------------------
    # 8. SYSTEM ARCHITECTURE
    # ---------------------------------------------------------
    add_h1("8. System Architecture")
    add_p("StudentSphere follows a decoupled, multi-tier architecture in which a lightweight single-page frontend communicates with dedicated backend services and four independent public cloud platforms.")

    add_h2("8.1 Architecture Components")
    add_num("1.", "Client Presentation Tier: The HTML5/CSS3/JavaScript SPA running on port 3000. It handles state management, optimistic UI updates, and reactive cloud listeners.")
    add_num("2.", "Node.js HTTP Server & Cloud Functions: The backend compute engine serving static files and REST endpoints at /api/mongodb/*.")
    add_num("3.", "Auth0 Identity Platform (IDaaS): Manages institutional authentication, issuing signed JWT tokens and handling Google OAuth federation.")
    add_num("4.", "Firebase Cloud Firestore (BaaS): Stores real-time student collections with continuous client stream listeners.")
    add_num("5.", "Firebase Cloud Storage (STaaS): Hosts persistent cloud object files (students.json) in Google Cloud.")
    add_num("6.", "MongoDB Atlas (DBaaS): Stores structured NoSQL student documents in cloud database studentsphere_db.")
    add_num("7.", "Dropbox API v2 (STaaS): Stores automated offsite disaster recovery backup files in Dropbox cloud accounts.")

    add_h2("8.2 Architecture Diagram")
    add_image_figure("fig_architecture.png", "Figure 1: Multi-Cloud Architecture of StudentSphere.")

    add_h2("8.3 Working Principle")
    add_p("When an administrator opens the application, the client verifies authentication status with Auth0. If unauthenticated, the user is redirected to Auth0 Universal Login or presents the institutional sign-in modal. Upon authentication, Auth0 returns verified user claims.")
    add_p("The web client immediately initializes student records from local cache for instant display, then subscribes to Firebase Firestore using an onSnapshot listener. When an administrator creates, modifies, or deletes a student record, the client updates the UI optimistically, commits the change to Firestore, uploads the updated JSON dataset to Firebase Storage, dispatches the document to MongoDB Atlas via the Node.js REST API, and uploads a backup to Dropbox.")

    # ---------------------------------------------------------
    # 9. SYSTEM DESIGN AND MODULES
    # ---------------------------------------------------------
    add_h1("9. System Design and Modules")
    add_p("The application is organized into modular services according to the responsibilities of the integrated cloud providers.")

    add_h2("9.1 Authentication & Identity Module")
    add_p("This module encapsulates user authentication using the @auth0/auth0-spa-js library and Firebase Auth. It manages user tokens, supports email/password login and Google OAuth single sign-on, and updates UI status badges upon successful authentication.")

    add_h2("9.2 Student Record Management Module")
    add_p("This module implements full CRUD (Create, Read, Update, Delete) operations for student records. Each student record contains a Student ID, Full Name, Age, and Department. The module validates inputs, handles optimistic in-memory updates, and maintains consistent state across storage engines.")

    add_h2("9.3 Multi-Engine & Hybrid Cloud Storage Module")
    add_p("This module provides a unified data access layer coordinating student persistence across multiple cloud storage engines. The storage engines are summarized below:")

    tbl_engines = doc.add_table(rows=5, cols=3)
    set_table_borders(tbl_engines)
    tbl_engines.alignment = WD_TABLE_ALIGNMENT.CENTER
    eng_headers = ["Storage Option", "Technology & Model", "Characteristics"]
    for c_idx, h_text in enumerate(eng_headers):
        cell = tbl_engines.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_background(cell, "F1F5F9")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)

    eng_data = [
        ("MongoDB Atlas", "MongoDB Atlas (DBaaS)", "Managed NoSQL document persistence with BSON querying and secure server-side connection pooling."),
        ("Firestore", "Google Cloud Firestore (BaaS)", "Serverless real-time document database with reactive onSnapshot stream listeners."),
        ("Firebase Storage", "Google Cloud Storage (STaaS)", "Persistent cloud object storage bucket hosting students.json for global access."),
        ("Local Storage", "Browser Web Storage API", "Zero-latency optimistic local cache ensuring the UI never hangs during network delays.")
    ]
    for r_idx, (c1, c2, c3) in enumerate(eng_data):
        row = tbl_engines.rows[r_idx + 1]
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
        for cell in row.cells:
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)

    add_h2("9.4 Dropbox Cloud Export and Backup Module")
    add_p("This module interfaces with the Dropbox Files API v2. It validates the user's Dropbox access token, checks account connection status via /2/users/get_current_account, serializes student records into formatted JSON, and uploads the dataset to /students.json using mode=overwrite.")

    add_h2("9.5 Search, Filter, and Analytics Dashboard Module")
    add_p("This module provides instant client-side filtering across student identifiers, full names, and academic departments. It dynamically computes real-time KPI metrics—Total Registered Students, Average Student Age, and Total Academic Departments—without requiring additional backend queries.")

    add_h2("9.6 API and Error Handling Module")
    add_p("This module defines the RESTful endpoints used by the application, listed below. The backend processes requests and returns structured JSON responses. Robust error handling transforms low-level database and network errors into clear toast messages for administrators.")

    add_h3("Node.js Backend Server (http://localhost:3000):")
    tbl_node_api = doc.add_table(rows=6, cols=4)
    set_table_borders(tbl_node_api)
    tbl_node_api.alignment = WD_TABLE_ALIGNMENT.CENTER
    api_headers = ["Method", "Endpoint", "Query / Body", "Description"]
    for c_idx, h_text in enumerate(api_headers):
        cell = tbl_node_api.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_background(cell, "F1F5F9")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)

    node_api_data = [
        ("GET", "/api/mongodb/students", "None", "Fetches all student records from MongoDB Atlas cluster."),
        ("POST", "/api/mongodb/student", "JSON student object", "Creates or updates a student record in MongoDB Atlas."),
        ("DELETE", "/api/mongodb/student", "?id={studentId}", "Deletes a student record from MongoDB Atlas."),
        ("POST", "/api/mongodb/sync", "JSON student array", "Synchronizes complete student roster into MongoDB Atlas."),
        ("POST", "/api/mongodb/test", "None", "Tests connectivity and pings MongoDB Atlas cluster.")
    ]
    for r_idx, row_values in enumerate(node_api_data):
        row = tbl_node_api.rows[r_idx + 1]
        for c_idx, val in enumerate(row_values):
            row.cells[c_idx].text = val
            row.cells[c_idx].paragraphs[0].runs[0].font.size = Pt(9.5)

    add_h3("Dropbox Cloud Service (https://api.dropboxapi.com):")
    tbl_dbx_api = doc.add_table(rows=3, cols=4)
    set_table_borders(tbl_dbx_api)
    tbl_dbx_api.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c_idx, h_text in enumerate(api_headers):
        cell = tbl_dbx_api.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_background(cell, "F1F5F9")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)

    dbx_api_data = [
        ("POST", "/2/files/upload", "Binary stream of students.json", "Uploads student roster backup to Dropbox."),
        ("POST", "/2/users/get_current_account", "None (Authorization header)", "Validates Dropbox token and account connection.")
    ]
    for r_idx, row_values in enumerate(dbx_api_data):
        row = tbl_dbx_api.rows[r_idx + 1]
        for c_idx, val in enumerate(row_values):
            row.cells[c_idx].text = val
            row.cells[c_idx].paragraphs[0].runs[0].font.size = Pt(9.5)

    add_h2("9.7 Data Flow Diagram")
    add_image_figure("fig_dataflow.png", "Figure 2: Data Flow Diagram of Authentication, Student Records Dispatch, and Multi-Cloud Sync.")

    add_h2("9.8 Data Structures")
    add_p("Each storage engine organizes student records according to its data model. MongoDB stores structured BSON documents, Firestore stores documents with real-time listeners, and Dropbox/Firebase Storage store full JSON arrays.")
    add_image_figure("fig_datastructures.png", "Figure 3: Data Structures Used Across Cloud Storage Engines.")

    # ---------------------------------------------------------
    # 10. IMPLEMENTATION & 11. SCREENSHOTS
    # ---------------------------------------------------------
    doc.add_page_break()
    add_h1("10. Implementation")
    add_p("The frontend was implemented using pure HTML5, modern CSS3, and JavaScript ES modules. The backend was constructed with Node.js and Google Cloud Firebase Cloud Functions. Dependencies were managed via npm, and each service was configured to communicate with its respective cloud provider.")

    add_h2("10.1 Backend and Frontend Setup")
    add_p("A Node.js project was initialized with ES module support (\"type\": \"module\"). The Node.js server (server.js) listens on port 3000, serving static web assets and defining REST endpoints at /api/mongodb/*. Firebase Hosting serves frontend assets in production and routes API requests to Cloud Functions.")

    add_h2("10.2 Authentication Implementation")
    add_p("Auth0 was configured with tenant domain dev-58o1wuwbx3qv1hfn.us.auth0.com. The frontend initializes the Auth0 SPA SDK in auth0-service.js. Users can authenticate with email/password credentials or click 'Continue with Google' to initiate Google OAuth federation.")
    add_image_figure("fig_login.png", "Figure 4: StudentSphere Authentication Screen (Email/Password & Google SSO).")

    add_h2("10.3 MongoDB Atlas Integration")
    add_p("The Node.js backend connects to MongoDB Atlas using the official mongodb driver and a mongodb+srv:// connection string. Connection pooling ensures high-throughput database interactions. Student documents contain id, name, age, and department. Free-tier M0 Atlas clusters can enter a paused state after inactivity, which must be resumed before database queries can execute.")
    add_image_figure("fig_dashboard.png", "Figure 5: Main Dashboard Displaying Real-Time Student Metrics and Department Roster.")

    add_h2("10.4 Firebase Cloud Firestore & Storage Integration")
    add_p("The Firebase Modular SDK (v10.12.0) is configured in firebase-config.js. The web client subscribes to student records using Firestore's onSnapshot listener, ensuring changes made on any terminal appear instantly across all clients. Concurrently, the complete roster is written to Google Firebase Storage bucket website-82bc7.firebasestorage.app as students.json.")
    add_image_figure("fig_add_student.png", "Figure 6: Student Profile Creation Dialog with Field Validation.")

    add_h2("10.5 Dropbox API Integration")
    add_p("The Dropbox integration in dropbox-service.js communicates directly with the Dropbox Files API v2. A generated OAuth access token is passed in the Authorization header. When student records are updated, the entire student list is serialized as formatted JSON and uploaded to Dropbox.")
    add_image_figure("fig_details.png", "Figure 7: Student Information and Academic Profile Modal.")

    add_h2("10.6 Cloud Service Models Used")
    add_p("StudentSphere leverages four primary cloud service models, each fulfilling a specialized role:")
    tbl_models = doc.add_table(rows=6, cols=4)
    set_table_borders(tbl_models)
    tbl_models.alignment = WD_TABLE_ALIGNMENT.CENTER
    model_headers = ["Cloud Service", "Provider", "Cloud Model", "Role in StudentSphere"]
    for c_idx, h_text in enumerate(model_headers):
        cell = tbl_models.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_background(cell, "F1F5F9")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)

    model_data = [
        ("Auth0", "Okta", "IDaaS", "Identity management, Universal Login, and Google OAuth SSO."),
        ("MongoDB Atlas", "MongoDB Inc.", "DBaaS", "Managed NoSQL document database for structured records."),
        ("Firebase Firestore", "Google Cloud", "BaaS", "Serverless real-time database with instant client stream listeners."),
        ("Firebase Storage", "Google Cloud", "STaaS", "Cloud object storage bucket for persistent students.json."),
        ("Dropbox API", "Dropbox", "STaaS", "Offsite file storage and automated JSON backup snapshots.")
    ]
    for r_idx, row_values in enumerate(model_data):
        row = tbl_models.rows[r_idx + 1]
        for c_idx, val in enumerate(row_values):
            row.cells[c_idx].text = val
            row.cells[c_idx].paragraphs[0].runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # ---------------------------------------------------------
    # 11. APPLICATION SCREENSHOTS AND RESULTS
    # ---------------------------------------------------------
    add_h1("11. Application Screenshots and Results")
    add_p("This section documents the actual user interface and functionality of StudentSphere.")

    add_h2("11.1 Authentication & Login Interface")
    add_p("Unauthenticated users are greeted by the authentication screen shown in Figure 4, supporting email/password authentication, registration, and Google OAuth sign-in.")

    add_h2("11.2 Main Student Dashboard & Metrics")
    add_p("Upon successful login, administrators access the primary dashboard (Figure 5) showing live KPI counters (Total Students, Average Student Age, Total Departments) and the interactive student directory table.")

    add_h2("11.3 Search and Department Filter Operations")
    add_p("The search input filters student records in real time across Student ID, Full Name, and Department. Selecting a department from the dropdown isolates the corresponding roster immediately, as shown in Figure 9.")
    add_image_figure("fig_search.png", "Figure 9: Real-Time Search and Department Filtering Interface.")

    add_h2("11.4 Record Deletion Safety Modal")
    add_p("Clicking 'Delete' on any student record opens a dedicated safety confirmation dialog to prevent accidental data loss.")
    add_image_figure("fig_delete.png", "Figure 8: Record Deletion Safety Confirmation Dialog.")

    add_h2("11.5 Dropbox Cloud Storage Synchronization")
    add_p("The system settings modal includes a dedicated Dropbox tab (Figure 10). Administrators can paste an OAuth access token, verify connection to the Dropbox account, and trigger automated JSON backup uploads to /students.json.")
    add_image_figure("fig_settings_dropbox.png", "Figure 10: Dropbox Cloud Storage Integration and Token Management.")

    add_h2("11.6 MongoDB Atlas Database Configuration")
    add_p("The MongoDB Atlas configuration tab (Figure 11) allows administrators to verify cluster connectivity, view database and collection names, and trigger bulk synchronization of student records from the browser to the Atlas cluster.")
    add_image_figure("fig_settings_mongo.png", "Figure 11: MongoDB Atlas Cloud Database Configuration and Health Diagnostics.")

    doc.add_page_break()

    # ---------------------------------------------------------
    # 12. TESTING AND RESULTS
    # ---------------------------------------------------------
    add_h1("12. Testing and Results")
    add_p("Testing was conducted to verify application features, authentication flows, database persistence, and multi-cloud synchronization.")

    tbl_test = doc.add_table(rows=16, cols=4)
    set_table_borders(tbl_test)
    tbl_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Test Case", "Expected Result", "Actual Result", "Status"]
    for c_idx, h_text in enumerate(test_headers):
        cell = tbl_test.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_background(cell, "F1F5F9")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)

    test_data = [
        ("Start Node.js Application Server", "Server initializes on port 3000 without errors", "Server running at http://localhost:3000", "Passed"),
        ("User Sign-In with Email & Password", "Auth service validates credentials and loads dashboard", "Authenticated successfully; dashboard loaded", "Passed"),
        ("Single Sign-On with Google (Auth0)", "Redirects to Google consent and returns verified claims", "OAuth consent completed; session active", "Passed"),
        ("Real-Time Dashboard KPI Calculation", "Counters compute total students, average age, and departments", "Calculated: 5 students, 21 yrs avg age", "Passed"),
        ("Create New Student Record", "Record is validated and rendered optimistically in table", "Student STU-106 created and rendered", "Passed"),
        ("Firestore Real-Time Synchronization", "Changes in one client reflect on secondary clients instantly", "Records updated instantly across windows", "Passed"),
        ("Firebase Cloud Storage JSON Upload", "Full student array written to website-82bc7 bucket", "File students.json uploaded successfully", "Passed"),
        ("Live Search by Student Name / ID", "Table dynamically filters records matching query substring", "Query 'Data' isolated Data Science student", "Passed"),
        ("Filter by Academic Department", "Dropdown selects department and filters roster accordingly", "Filter isolated Computer Science students", "Passed"),
        ("View Student Details Inspection", "Modal opens displaying student ID, name, age, department", "Modal displayed correct profile details", "Passed"),
        ("Delete Student Record with Confirm", "Confirmation dialog prompts user and removes record", "Record deleted from UI and cloud databases", "Passed"),
        ("MongoDB Atlas Connection Ping", "POST /api/mongodb/test returns 200 OK with ping latency", "Ping returned { success: true, ping: 1 }", "Passed"),
        ("MongoDB Atlas Batch Sync", "POST /api/mongodb/sync writes student roster to Atlas", "Documents inserted into students collection", "Passed"),
        ("Dropbox API v2 Cloud File Backup", "Dataset uploaded to /students.json with overwrite mode", "File uploaded to Dropbox successfully", "Passed"),
        ("Invalid Dropbox Token Handling", "API returns descriptive error alert via toast notification", "Toast: 'Invalid or expired Dropbox token'", "Passed")
    ]
    for r_idx, row_values in enumerate(test_data):
        row = tbl_test.rows[r_idx + 1]
        for c_idx, val in enumerate(row_values):
            row.cells[c_idx].text = val
            row.cells[c_idx].paragraphs[0].runs[0].font.size = Pt(9)
            if c_idx == 3:
                row.cells[c_idx].paragraphs[0].runs[0].font.bold = True

    add_h2("12.1 Functional Testing")
    add_p("Functional testing confirmed that all primary features—student creation, details viewing, deletion prompts, live search, and department filtering—perform reliably according to specifications.")

    add_h2("12.2 Authentication Testing")
    add_p("Authentication testing verified that protected actions require valid session tokens, and that unauthenticated users cannot view or manipulate student records.")

    add_h2("12.3 Database Testing")
    add_p("Database testing verified that student documents are correctly created, updated, and deleted in MongoDB Atlas and Google Cloud Firestore. Firestore listeners updated client interfaces without manual refreshes.")

    add_h2("12.4 File Storage & Cloud Export Testing")
    add_p("File export testing verified that valid JSON files are generated and uploaded to Google Firebase Storage and Dropbox with correct syntax and write permissions.")

    add_h2("12.5 Result Discussion")
    add_p("The application demonstrates how authentication, multi-cloud databases, and cloud file storage can be integrated through a single web portal. During testing, it was noted that MongoDB Atlas free-tier clusters can enter a paused state after inactivity, requiring resumption before SRV connections succeed. Optimistic UI caching ensured that temporary cloud latency never froze the user interface.")

    # ---------------------------------------------------------
    # 13. ADVANTAGES & 14. LIMITATIONS
    # ---------------------------------------------------------
    add_h1("13. Advantages")
    add_num("1.", "Centralized Student Repository: Provides a unified administrative portal accessible from any desktop or mobile browser.")
    add_num("2.", "Multi-Cloud Resilience: Distributes workloads across Auth0, Google Cloud (Firestore & Storage), MongoDB Atlas, and Dropbox, eliminating single-vendor downtime risk.")
    add_num("3.", "Zero-Latency UI: Optimistic caching renders user actions in under 50 milliseconds while background sync occurs asynchronously.")
    add_num("4.", "Real-Time Updates: Firestore listeners update connected clients instantaneously without polling.")
    add_num("5.", "Enterprise Authentication: Auth0 provides secure identity management, ensuring user credentials never touch local servers.")
    add_num("6.", "Automated Offsite Backup: Student rosters are backed up to Dropbox as standardized JSON files for disaster recovery.")
    add_num("7.", "Decoupled Architecture: Frontend and backend services operate independently, simplifying maintenance.")
    add_num("8.", "Extensibility: Additional student attributes, academic grades, and course modules can be added easily.")

    add_h1("14. Limitations")
    add_bullet("The application depends on internet connectivity for cloud database synchronization.")
    add_bullet("Cloud service access depends on valid API tokens, permissions, and network whitelists.")
    add_bullet("Free-tier MongoDB Atlas clusters can pause after periods of inactivity and must be resumed before use.")
    add_bullet("Dropbox access tokens must be regenerated or refreshed periodically.")
    add_bullet("Dropbox synchronization currently pushes files outward but does not parse manual external edits back into the database.")
    add_bullet("Cloud service usage is subject to free-tier storage and API call quotas.")
    add_bullet("The current implementation focuses on administrative access rather than differentiated multi-tier student/faculty roles.")
    add_bullet("The local development proxy setup runs locally and is not automatically accessible over the public internet without hosting deployment.")

    # ---------------------------------------------------------
    # 15. FUTURE ENHANCEMENTS, 16. CONCLUSION, 17. REFERENCES
    # ---------------------------------------------------------
    add_h1("15. Future Enhancements")
    add_num("1.", "Implement Role-Based Access Control (RBAC) distinguishing between Student, Faculty, and Admin roles.")
    add_num("2.", "Add course enrollment tracking, credit hours, and faculty advisor assignments.")
    add_num("3.", "Provide one-click export of student rosters to Microsoft Excel (.xlsx) and CSV formats.")
    add_num("4.", "Integrate academic grading scales with automated GPA and CGPA computation.")
    add_num("5.", "Add student photo upload and identification card storage via Firebase Cloud Storage.")
    add_num("6.", "Implement bi-directional Dropbox synchronization using webhook notifications.")
    add_num("7.", "Integrate SMS and email notification services (e.g., Twilio / SendGrid) for institutional announcements.")
    add_num("8.", "Develop a self-service student portal where students can log in to view their personal academic records.")
    add_num("9.", "Add dynamic dark/light theme switching with saved user preferences.")
    add_num("10.", "Package backend services into Docker containers and deploy to Google Cloud Run.")
    add_num("11.", "Add automated unit and end-to-end testing with GitHub Actions CI/CD pipelines.")
    add_num("12.", "Implement comprehensive audit logging to track all administrative record modifications.")

    p_prop = doc.add_paragraph()
    p_prop.paragraph_format.space_before = Pt(4)
    p_prop.paragraph_format.space_after = Pt(10)
    r_pr = p_prop.add_run("These are proposed improvements and are not described as completed features.")
    r_pr.font.italic = True
    r_pr.font.size = Pt(10)

    add_h1("16. Conclusion")
    add_p("StudentSphere was developed as a cloud computing project to demonstrate the practical integration of identity, database, backend, and storage services in a single academic application.")
    add_p("HTML5 and CSS3 provide an intuitive, responsive user interface, while Node.js and Google Cloud Functions handle backend routing. Auth0 is used for authentication and Google single sign-on, MongoDB Atlas and Firebase Firestore store student records, and Firebase Storage and the Dropbox API store persistent JSON datasets. Together, they demonstrate the IDaaS, DBaaS, BaaS, and STaaS cloud service models.")
    add_p("The project provides practical knowledge of full-stack web development, serverless microservices, token-based authentication, NoSQL database operations, real-time client synchronization, environment configuration, and cloud storage integration.")
    add_p("The implementation can be extended with features such as course enrollment, GPA calculation, Excel exports, and containerized cloud deployment. Overall, the project provides a practical demonstration of cloud computing concepts through a multi-cloud student records and information management platform.")

    add_h1("17. References")
    refs = [
        "Auth0 Documentation. https://auth0.com/docs",
        "Google Cloud Firebase Documentation. https://firebase.google.com/docs",
        "Firebase Cloud Firestore Documentation. https://firebase.google.com/docs/firestore",
        "Firebase Cloud Storage Documentation. https://firebase.google.com/docs/storage",
        "Firebase Admin SDK Documentation. https://firebase.google.com/docs/admin/setup",
        "Node.js Official Documentation. https://nodejs.org/docs/latest/api/",
        "MongoDB Atlas Documentation. https://www.mongodb.com/docs/atlas/",
        "MongoDB Node.js Driver Documentation. https://www.mongodb.com/docs/drivers/node/current/",
        "Dropbox API Documentation. https://www.dropbox.com/developers/documentation/http/overview",
        "npm Documentation. https://docs.npmjs.com/",
        "MDN Web Docs: Modern JavaScript & Fetch API. https://developer.mozilla.org/",
        "RFC 6749: The OAuth 2.0 Authorization Framework. https://datatracker.ietf.org/doc/html/rfc6749"
    ]
    for idx, ref in enumerate(refs):
        add_num(f"{idx+1}.", ref)

    docx_path = os.path.join(WORKSPACE, "StudentSphere_Project_Report.docx")
    doc.save(docx_path)
    print(f"DOCX successfully generated at: {docx_path}")

if __name__ == "__main__":
    build_docx()
