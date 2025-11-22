# API Documentation

Base URL: `http://localhost:5000/api` (development) or `https://your-domain.up.railway.app/api` (production)

## Endpoints

### Health Check

Check if the API and database are operational.

```
GET /api/health
```

**Response:**

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

### Get All Entities

Retrieve all entities with translations.

```
GET /api/entities
```

**Query Parameters:**

- `lang` (optional): Language code (`es`, `en`, etc.). Default: `es`
- `type` (optional): Filter by entity type (e.g., `project`)
- `category` (optional): Filter by category

**Example:**

```
GET /api/entities?lang=en&type=project
```

**Response:**

```json
[
  {
    "id": 1,
    "slug": "portfolio",
    "type": "project",
    "category": "proyectos",
    "tags": ["HTML", "CSS", "JS"],
    "title": "Portfolio",
    "subtitle": "WebPage - 2025",
    "description": "This is my personal portfolio...",
    "summary": "This is my personal portfolio...",
    "content": { ... },
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  }
]
```

---

### Get Entity by Slug

Retrieve a single entity by its slug, with all available translations.

```
GET /api/entities/<slug>
```

**Query Parameters:**

- `lang` (optional): Preferred language. Default: `es`

**Example:**

```
GET /api/entities/portfolio?lang=en
```

**Response:**

```json
{
  "id": 1,
  "slug": "portfolio",
  "type": "project",
  "category": "proyectos",
  "tags": ["HTML", "CSS", "JS"],
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00",
  "translations": {
    "es": {
      "title": "Portafolio",
      "subtitle": "WebPage - 2025",
      "description": "...",
      "summary": "...",
      "content": { ... }
    },
    "en": {
      "title": "Portfolio",
      "subtitle": "WebPage - 2025",
      "description": "...",
      "summary": "...",
      "content": { ... }
    }
  },
  "current": {
    "title": "Portfolio",
    "subtitle": "WebPage - 2025",
    "description": "...",
    "summary": "...",
    "content": { ... }
  }
}
```

---

### Get Available Languages

Get a list of all available languages in the system.

```
GET /api/languages
```

**Response:**

```json
{
  "languages": ["es", "en"],
  "count": 2
}
```

---

### Get Categories

Get all unique categories used in entities.

```
GET /api/categories
```

**Query Parameters:**

- `type` (optional): Filter by entity type

**Response:**

```json
{
  "categories": ["proyectos", "trabajo"],
  "count": 2
}
```

---

### Get Tags

Get all tags with usage counts.

```
GET /api/tags
```

**Response:**

```json
{
  "tags": [
    { "tag": "Python", "count": 3 },
    { "tag": "Flask", "count": 2 },
    { "tag": "React", "count": 1 }
  ],
  "total": 3
}
```

---

## CORS Configuration

The API allows requests from:

- `http://localhost:3000` (React default)
- `http://localhost:5173` (Vite default)
- Custom origins via `CORS_ORIGINS` environment variable

**Allowed Methods:** GET, POST, PUT, DELETE, OPTIONS

**Allowed Headers:** Content-Type, Authorization

---

## Error Responses

### 404 Not Found

```json
{
  "error": "Not found",
  "message": "Entity not found"
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal server error",
  "message": "Error details..."
}
```

---

## Testing the API

### Using curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Get all entities
curl http://localhost:5000/api/entities?lang=es

# Get specific entity
curl http://localhost:5000/api/entities/portfolio?lang=en
```

### Using the test script:

```bash
python test_api.py
```

### Using your browser:

Just open: `http://localhost:5000/api/entities?lang=es`
