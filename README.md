# Inventory API

This project implements the REST API described in the exam requirements using FastAPI, SQLAlchemy, and SQLite.

## Project structure

- `exam_project/database.py` - database setup and session management
- `exam_project/models.py` - SQLAlchemy models for categories and books
- `exam_project/schemas.py` - Pydantic request/response models
- `exam_project/crud.py` - database helper functions
- `exam_project/main.py` - FastAPI routes and validation

## Run locally

```bash
python -m pip install -r requirements.txt
uvicorn exam_project.main:app --reload
```

## Example endpoints

- `POST /categories/` - add a category
- `GET /categories/` - list all categories
- `POST /books/` - add a book linked to an existing category
- `GET /books/` - list books
- `GET /books/{book_id}` - fetch one book
- `PUT /books/{book_id}` - update book details
- `DELETE /books/{book_id}` - delete a book

## Validation behavior

- Returns 400 when a category does not exist while creating a book
- Returns 400 when a book ISBN already exists
- Returns 404 for missing books
