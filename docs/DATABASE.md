# Database Schema Documentation

## Overview

This application uses a PostgreSQL database with 3 main tables. The term "Entity" is used as a generic CMS pattern, but **currently stores portfolio projects only**.

---

## Tables

### 1. `entities` (Portfolio Projects)

Stores the core project information.

| Column       | Type        | Description                                                            |
| ------------ | ----------- | ---------------------------------------------------------------------- |
| `id`         | INTEGER     | Primary key, auto-increment                                            |
| `slug`       | VARCHAR(64) | Unique URL-friendly identifier (e.g., "portfolio", "dashboard-ventas") |
| `type`       | VARCHAR(32) | Entity type (currently always "project")                               |
| `meta`       | JSON        | Metadata: category, tags, images, etc.                                 |
| `created_at` | TIMESTAMP   | Creation timestamp                                                     |
| `updated_at` | TIMESTAMP   | Last update timestamp                                                  |

**Indexes:**

- Primary key on `id`
- Unique index on `slug`

**Example Row:**

```json
{
  "id": 1,
  "slug": "portfolio",
  "type": "project",
  "meta": {
    "category": "proyectos",
    "tags": ["HTML", "CSS", "JS", "Design"],
    "images": {
      "desktop": "images/mockups/2.jpg",
      "mobile": "images/mockups/1.jpg"
    }
  },
  "created_at": "2025-01-01 12:00:00",
  "updated_at": "2025-01-01 12:00:00"
}
```

---

### 2. `translations` (Multilingual Content)

Stores translations for each entity in multiple languages.

| Column        | Type         | Description                      |
| ------------- | ------------ | -------------------------------- |
| `id`          | INTEGER      | Primary key, auto-increment      |
| `entity_id`   | INTEGER      | Foreign key to `entities.id`     |
| `lang`        | VARCHAR(8)   | Language code (e.g., "es", "en") |
| `title`       | VARCHAR(128) | Project title                    |
| `subtitle`    | VARCHAR(128) | Project subtitle                 |
| `description` | TEXT         | Full description (supports HTML) |
| `summary`     | TEXT         | Short summary                    |
| `content`     | JSON         | Additional structured content    |

**Indexes:**

- Primary key on `id`
- Foreign key on `entity_id` → `entities.id` (CASCADE DELETE)
- Index on `lang` for filtering

**Example Rows:**

```json
[
  {
    "id": 1,
    "entity_id": 1,
    "lang": "es",
    "title": "Portafolio",
    "subtitle": "WebPage - 2025",
    "description": "Este es mi portafolio personal...",
    "summary": "Este es mi portafolio personal...",
    "content": {}
  },
  {
    "id": 2,
    "entity_id": 1,
    "lang": "en",
    "title": "Portfolio",
    "subtitle": "WebPage - 2025",
    "description": "This is my personal portfolio...",
    "summary": "This is my personal portfolio...",
    "content": {}
  }
]
```

---

### 3. `users` (Authentication)

Stores user information for Google OAuth authentication and role-based access control.

| Column        | Type         | Description                             |
| ------------- | ------------ | --------------------------------------- |
| `id`          | INTEGER      | Primary key, auto-increment             |
| `email`       | VARCHAR(255) | User email (unique)                     |
| `name`        | VARCHAR(100) | First name                              |
| `surname`     | VARCHAR(100) | Last name                               |
| `country`     | VARCHAR(100) | User country (from headers)             |
| `picture_url` | VARCHAR(300) | Google profile picture URL              |
| `role`        | VARCHAR(50)  | User role: "admin", "visitor", "banned" |
| `is_verified` | BOOLEAN      | Email verification status               |
| `last_login`  | TIMESTAMP    | Last login timestamp                    |

**Indexes:**

- Primary key on `id`
- Unique index on `email`

**Example Row:**

```json
{
  "id": 1,
  "email": "admin@example.com",
  "name": "Rafael",
  "surname": "Ortiz",
  "country": "VE",
  "picture_url": "https://lh3.googleusercontent.com/...",
  "role": "admin",
  "is_verified": true,
  "last_login": "2025-01-01 14:30:00"
}
```

**Roles:**

- `admin` - Can access admin panel, create/edit/delete entities
- `visitor` - Basic authenticated user (not currently used)
- `banned` - Blocked from accessing the system

---

## Relationships

```
entities (1) ←──── (N) translations
   ↓
   One entity (project) can have multiple translations (one per language)
   Deleting an entity cascades to delete all its translations

users
   ↓
   Independent table for authentication
   No direct relationship with entities
```

**Visual Schema:**

```
┌─────────────────────┐
│     entities        │
├─────────────────────┤
│ id (PK)             │
│ slug (UNIQUE)       │
│ type                │
│ meta (JSON)         │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1:N
           │
┌──────────▼──────────┐
│   translations      │
├─────────────────────┤
│ id (PK)             │
│ entity_id (FK)      │
│ lang                │
│ title               │
│ subtitle            │
│ description         │
│ summary             │
│ content (JSON)      │
└─────────────────────┘

┌─────────────────────┐
│      users          │
├─────────────────────┤
│ id (PK)             │
│ email (UNIQUE)      │
│ name                │
│ surname             │
│ country             │
│ picture_url         │
│ role                │
│ is_verified         │
│ last_login          │
└─────────────────────┘
```

---

## Current Data Example

### Typical Portfolio Setup

**3 Entities (Projects):** (11-01-2025)

1. `portfolio` - Personal portfolio website
2. `dashboard-ventas` - Sales dashboard (Power BI)
3. `api-scraper_bcv` - BCV rate scraper API

**6 Translations (2 per project):**

- Spanish (es) version for each
- English (en) version for each

**1 User:**

- Admin account (me)

---

## JSON Field Structures

### `entities.meta` Structure

```json
{
  "category": "proyectos", // Category name
  "tags": ["Python", "Flask"], // Array of technology tags
  "images": {
    // Optional image URLs
    "desktop": "images/mockups/1.jpg",
    "mobile": "images/mockups/2.jpg"
  }
}
```

### `translations.content` Structure

```json
{
  "images": {
    // Duplicate of entity.meta.images
    "desktop": "images/mockups/1.jpg",
    "mobile": "images/mockups/2.jpg"
  },
  "category": "proyectos" // Duplicate of entity.meta.category
}
```

_Note: Some data is duplicated between `meta` and `content` for historical reasons. Consider normalizing in a future refactor._

---

## Queries Reference

### Get all projects with Spanish translations

```sql
SELECT e.*, t.title, t.description
FROM entities e
JOIN translations t ON e.id = t.entity_id
WHERE t.lang = 'es'
ORDER BY e.created_at DESC;
```

### Get project by slug with all translations

```sql
SELECT e.*, t.lang, t.title, t.subtitle, t.description
FROM entities e
LEFT JOIN translations t ON e.id = t.entity_id
WHERE e.slug = 'portfolio';
```

### Get all available languages

```sql
SELECT DISTINCT lang FROM translations;
```

### Get all tags across all projects

```sql
SELECT DISTINCT jsonb_array_elements_text(meta->'tags') as tag
FROM entities
WHERE meta->'tags' IS NOT NULL;
```

---

## Database Initialization

Tables are created automatically by SQLAlchemy when the application starts:

```python
# In backend/app.py
with app.app_context():
    db.create_all()
```

Models are defined in:

- `backend/models/entity.py`
- `backend/models/translation.py`
- `backend/models/user.py`

---

## Migration & Seeding

To populate the database with initial data from `data/gallery.json`:

```bash
python scripts/migrate_gallery.py
```

This script:

1. Reads `data/gallery.json`
2. Creates entity records
3. Creates translation records for each language
4. Updates existing records if slug already exists

---

## Connection Info

The database connection is configured via environment variable:

```env
DATABASE_URL=postgresql://user:password@host:port/database
```

For local development with SQLite:

```env
DATABASE_URL=sqlite:///portfolio.db
```

---

## Notes

- **Cascade Deletes**: Deleting an entity automatically deletes all its translations
- **Language Flexibility**: Any 2-letter language code works (es, en, fr, de, etc.)
- **JSON Fields**: Use PostgreSQL's JSON capabilities for flexible metadata storage
- **Shared Database**: This app can coexist with other apps using the same PostgreSQL instance (different tables)
- **No UUID**: Uses integer IDs for simplicity; consider UUIDs for distributed systems

---

## Future Improvements

Potential schema enhancements:

- Add `published` boolean field to entities for draft/published state
- Add `order` field for manual sorting
- Normalize the `images` data (currently duplicated)
- Add `media` table for file uploads
- Add `categories` table instead of storing as strings
- Add entity versioning/history table
