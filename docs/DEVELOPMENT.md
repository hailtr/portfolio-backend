# Development Guide

## Quick Start

### First Time Setup

1. **Clone the repository and navigate to the directory**
   ```powershell
   cd portfolio-backend
   ```

2. **Create your environment file**
   ```powershell
   Copy-Item env.example .env
   ```
   Then edit `.env` with your actual credentials.

3. **Run the startup script**
   ```powershell
   .\start_dev.ps1
   ```
   
   This will automatically:
   - Create virtual environment if needed
   - Install dependencies
   - Activate venv
   - Start the Flask server

### Daily Development

**Option 1: Use the startup script (Recommended)**
```powershell
.\start_dev.ps1
```

**Option 2: Manual activation**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the application
python run.py
```

---

## Running the Application

### Development Server
```powershell
python run.py
```
- Runs on `http://localhost:5000`
- Auto-reload enabled
- Debug mode active

### Production-like Testing
```powershell
gunicorn wsgi:app --bind 0.0.0.0:8000
```

---

## Project Structure & Import System

### Why `run.py` and `wsgi.py`?

This project uses **standard Python packaging practices** to ensure it works everywhere:

```
portfolio-backend/
├── run.py          ← Development entry point
├── wsgi.py         ← Production entry point (Railway, Heroku, etc.)
├── backend/        ← Main package (importable as 'backend')
│   ├── __init__.py
│   ├── app.py      ← Flask app creation
│   ├── models/
│   ├── routes/
│   └── templates/
```

**How it works:**
1. `run.py` and `wsgi.py` add the project root to Python's path
2. This makes `backend` package importable
3. Works in development, production, Docker, Railway, etc.

**Why not run `backend/app.py` directly?**
- Running nested files breaks Python's import system
- Production servers need a proper entry point
- This is **standard Flask practice** (see Flask, Django, FastAPI projects)

---

## Common Tasks

### Install New Dependencies
```powershell
.\venv\Scripts\Activate.ps1
pip install package-name
pip freeze > requirements.txt
```

### Database Operations

**Reset database (careful!)**
```powershell
python run.py  # Will auto-create tables
```

**Run migrations (when you create them)**
```powershell
flask db upgrade
```

### Testing
```powershell
pytest
```

---

## Deployment

### Railway Deployment

Railway automatically detects:
- `Procfile` - Knows to run `gunicorn wsgi:app`
- `requirements.txt` - Installs dependencies
- Environment variables from Railway dashboard

**No special configuration needed!** The `wsgi.py` handles all the path setup.

### Environment Variables on Railway

Set these in Railway dashboard:
- `DATABASE_URL` (auto-set by Railway if you add PostgreSQL)
- `FLASK_SECRET_KEY`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `ADMIN_EMAIL`
- `FLASK_ENV=production`

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Activate virtual environment first
```powershell
.\venv\Scripts\Activate.ps1
```

### "ModuleNotFoundError: No module named 'backend'"
**Solution:** Use `run.py` instead of running `backend/app.py` directly
```powershell
python run.py  # ✅ Correct
python backend/app.py  # ❌ Wrong
```

### Database connection errors
1. Check `.env` has correct `DATABASE_URL`
2. Ensure PostgreSQL is running (or use SQLite for development)
3. Check logs for specific error messages

### Port already in use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <pid> /F
```

---

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep routes thin, business logic in services

---

## Need Help?

Check:
1. This guide (DEVELOPMENT.md)
2. Main README.md
3. Code comments
4. `.env.example` for configuration options


