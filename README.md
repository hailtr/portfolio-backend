# Dynamic AI-Driven Portfolio

## Overview
This project is a dynamic, AI-assisted portfolio designed to adapt its content to the visitor’s intent.  
It moves beyond traditional static portfolios by using AI to highlight the most relevant information for each visitor and automating content maintenance.

Originally built as a Single Page Application (SPA) with a JSON data source, it is now being re-architected with a Flask backend and a React frontend.  
The goal is to achieve a modular, maintainable, and intelligent structure capable of generating personalized experiences and printable, pixel-perfect CVs.

---

## Objectives
1. **Maintainability**  
   Transition from static content to a structured data model using JSON as cache and PostgreSQL as the main data store.  
   Updates should be made through data uploads rather than direct code edits.

2. **Intelligence**  
   Integrate AI capabilities (Azure AI or OpenAI) to let the portfolio interpret visitor intent and dynamically prioritize relevant information.

3. **Reliable PDF Rendering**  
   Replace client-side screenshots with server-side PDF generation to ensure consistent formatting and pagination.

4. **Design Consistency**  
   Preserve the current aesthetic while introducing modular CSS and componentized layouts.  
   Maintain a clear separation between the frontend (React) and backend (Flask).

---

## Architecture

### High-Level Diagram
React (Frontend) ───► Flask API ───► PostgreSQL
│ │
└──── JSON Cache ◄┘

yaml


**Frontend (React)**  
Handles user interface, routing, language switching, and dynamic rendering.  
May be hosted on Vercel, Netlify, or another global CDN.

**Backend (Flask)**  
Acts as the core logic layer for API handling, data retrieval, PDF generation, and AI processing.  
Deployed on Railway, using PostgreSQL as the database and JSON as a caching mechanism.

**Database (PostgreSQL)**  
Stores structured portfolio content such as projects, experiences, and metadata.  
Ensures persistence and supports multilingual data fields.

**Cache (JSON)**  
Serves as a lightweight, fast-access layer to minimize database reads and support offline or fallback rendering.

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| Frontend | React | UI, routing, dynamic rendering |
| Backend | Flask | API logic, AI integration, PDF generation |
| Database | PostgreSQL (Railway) | Structured data storage |
| Cache | JSON | Local or cloud cache for quick reads |
| AI Layer | Azure AI / OpenAI | Context-aware personalization |
| Deployment | Railway (backend), Vercel or Netlify (frontend) | Hosting and CI/CD pipeline |
| Styling | CSS Modules or Tailwind | Modular design system |

---

## Folder Structure
portfolio/
│
├── backend/
│ ├── app.py
│ ├── routes/
│ ├── services/
│ ├── models/
│ └── templates/
│
├── frontend/
│ ├── src/
│ ├── public/
│ ├── package.json
│ └── build/
│
└── README.md

yaml


---

## Data Flow
1. Visitor interacts with React frontend.
2. Frontend requests data from Flask API.
3. Flask retrieves information from the JSON cache; if stale or missing, it queries PostgreSQL.
4. Data is returned to React in a structured format and rendered dynamically.
5. AI components analyze visitor behavior or query context to adjust what is shown.
6. On demand, Flask generates PDFs directly from templates and serves them as downloadable resumes.

---

## Roadmap

### Phase 1 – Core Infrastructure
- Flask API with PostgreSQL and JSON cache.
- React frontend connected to API.
- Basic bilingual content (English/Spanish).
- Deployment to Railway and Vercel.

### Phase 2 – PDF Engine
- Server-side rendering for clean CV export.
- Dedicated multilingual templates.
- Resume versioning and customization.

### Phase 3 – AI Personalization
- Integration with Azure or OpenAI APIs.
- Context-aware recommendations.
- Adaptive content highlighting per visitor profile.

### Phase 4 – Design and Optimization
- Modular CSS refactor or Tailwind migration.
- Performance, SEO, and accessibility improvements.
- Optional chat-style assistant inside portfolio.

---

## Vision
The long-term vision is to create a self-maintaining, intelligent portfolio system capable of understanding who is visiting and what they are looking for.  
Rather than listing achievements, the portfolio should **converse** with the visitor—offering the most relevant information first and shaping the narrative dynamically.

---

## License
MIT License © Rafael Ortiz