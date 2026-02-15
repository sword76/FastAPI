# FastAPI Hotel Management API

A REST API for managing hotel information built with FastAPI framework.

## Overview

This project provides CRUD operations for hotel records:
- Retrieve hotels with filtering and pagination
- Create new hotel entries
- Update hotels (full and partial updates)
- Delete hotels

Currently uses in-memory storage with PostgreSQL infrastructure ready for future integration.

## Tech Stack

- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM (prepared for PostgreSQL)
- **Alembic** - Database migrations
- **Uvicorn** - ASGI server

## Project Structure

```
src/
├── main.py              # Application entry point
├── config.py            # Settings management
├── db.py                # Database setup
├── api/
│   ├── hotels.py        # Hotel endpoints
│   └── dependencies.py  # Pagination dependency
├── schemas/
│   └── hotels.py        # Pydantic models
├── models/
│   └── hotels.py        # SQLAlchemy ORM model
└── migrations/          # Alembic migrations
```

## Running the Application

Development mode with auto-reload:
```bash
uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

Production mode:
```bash
uvicorn src.main:app --host 127.0.0.1 --port 8000 --workers 3
```

## API Documentation

Swagger UI available at: `http://127.0.0.1:8000/docs`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /hotels | List hotels with filtering and pagination |
| POST | /hotels | Create a new hotel |
| PUT | /hotels/{id} | Full update of a hotel |
| PATCH | /hotels/{id} | Partial update of a hotel |
| DELETE | /hotels/{id} | Delete a hotel |
