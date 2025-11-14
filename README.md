# Portfolio Backend - Rafael Ortiz

## Overview
A full-stack portfolio application showcasing projects, experience, and skills for a Data Engineer.  
Built with a Flask backend and React frontend, this system provides a dynamic, maintainable portfolio with multilingual support, admin panel for content management, and server-side PDF generation for CVs.

The application features a clean separation between frontend and backend, with PostgreSQL as the primary data store and JSON caching for performance. Content is managed through an admin interface, eliminating the need for direct code edits.

---

## Features

### Implemented
- **Flask Backend API** - RESTful API with PostgreSQL database and JSON caching
- **React Frontend** - Modern, responsive UI with routing and language switching (ES/EN)
- **Admin Panel** - Content management interface for projects, experiences, and profile data
- **PDF CV Generation** - Server-side PDF rendering using WeasyPrint for pixel-perfect CVs
- **Multilingual Support** - Full bilingual content (English/Spanish) with dynamic language switching
- **Authentication** - Google OAuth integration for admin access
- **Caching & Performance** - Redis caching layer with fallback to in-memory cache
- **Rate Limiting** - API protection with configurable rate limits
- **Health Monitoring** - Comprehensive health check endpoints for services

### Future Enhancements
- **AI Personalization** - Context-aware content prioritization based on visitor intent
- **Advanced Analytics** - Visitor behavior tracking and insights
- **Chat Assistant** - Interactive portfolio assistant for visitor engagement

---

## Architecture

### High-Level Diagram
```
React (Frontend) ───► Flask API ───► PostgreSQL
│ │
└──── Redis Cache ◄┘
```

**Frontend (React)**  
Handles user interface, routing, language switching, and dynamic rendering.  
Hosted on Vercel with global CDN distribution.

**Backend (Flask)**  
Core API layer handling data retrieval, PDF generation, and admin operations.  
Deployed on Railway with PostgreSQL database and Redis caching.

**Database (PostgreSQL)**  
Stores structured portfolio content including projects, experiences, and multilingual translations.  
Ensures data persistence and supports complex queries.

**Cache (Redis/Memory)**  
Fast-access layer to minimize database reads and improve response times.  
Falls back to in-memory cache if Redis is unavailable.


---

## Data Flow
1. **Visitor Interaction** - User interacts with React frontend (hosted on Vercel)
2. **API Request** - Frontend makes requests to Flask API endpoints
3. **Cache Check** - Flask checks Redis/in-memory cache for data
4. **Database Query** - If cache miss, queries PostgreSQL for structured portfolio data
5. **Response** - Data returned as JSON to React frontend
6. **Rendering** - React dynamically renders content with language support
7. **PDF Generation** - On demand, Flask generates PDF CVs using WeasyPrint templates

---

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL database (or SQLite for local development)
- Redis (optional, for caching)

### Backend Setup
```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment file
Copy-Item env.example .env
# Edit .env with your database and API keys

# Run the application
python run.py
```

### Frontend Setup
```powershell
cd frontend
npm install
npm run dev
```

For detailed setup instructions, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

## Project Structure
```
portfolio-backend/
├── backend/              # Flask application
│   ├── app.py           # Main Flask app
│   ├── models/          # SQLAlchemy models
│   ├── routes/          # API routes (api, admin, cv, index)
│   ├── services/        # Business logic (cache, PDF, Cloudinary)
│   ├── templates/       # HTML templates for CV and admin
│   └── utils/           # Utilities (rate limiting, etc.)
├── frontend/            # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   └── config.js    # API configuration
│   └── public/          # Static assets
├── auth/                # Authentication (Google OAuth)
├── docs/                # Documentation
├── scripts/             # Utility scripts
└── data/                # JSON data files
```

## API Documentation
See [docs/API.md](docs/API.md) for complete API endpoint documentation.

## Deployment
- **Backend**: Deployed on Railway with PostgreSQL
- **Frontend**: Deployed on Vercel
- **Database**: PostgreSQL (Railway)
- **Cache**: Redis (not yet)

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | React + Vite | UI, routing, dynamic rendering |
| Backend | Flask | API logic, PDF generation, admin panel |
| Database | PostgreSQL | Structured data storage (Railway) |
| Cache | Redis / Memory | Fast data access layer |
| PDF Engine | WeasyPrint | Server-side CV generation |
| Authentication | Google OAuth | Admin access control |
| Deployment | Railway (backend), Vercel (frontend) | Hosting and CI/CD |
| Styling | CSS Modules | Component-based styling |

## Contributing
This is a personal portfolio project. For questions or suggestions, please open an issue.

## License
MIT License © Rafael Ortiz