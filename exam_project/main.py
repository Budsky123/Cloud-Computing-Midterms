from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .crud import (
    create_book,
    create_category,
    delete_book,
    get_book_by_id,
    get_books,
    get_categories,
    get_category_by_id,
    update_book,
)
from .database import Base, engine, get_db
from .models import Book, Category
from .schemas import BookCreate, BookRead, BookUpdate, CategoryCreate, CategoryRead

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory API")


@app.post("/categories/", response_model=CategoryRead)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    return create_category(db, category.name)


@app.get("/categories/", response_model=List[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)


@app.post("/books/", response_model=BookRead)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    category = get_category_by_id(db, book.category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")

    existing_isbn = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing_isbn:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book with this ISBN already exists")

    book_payload = book.model_dump()
    return create_book(db, book_payload)


@app.get("/books/", response_model=List[BookRead])
def list_books(db: Session = Depends(get_db)):
    return get_books(db)


@app.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=BookRead)
def update_book_by_id(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    if book_update.category_id is not None:
        category = get_category_by_id(db, book_update.category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")

    if book_update.isbn is not None:
        existing = db.query(Book).filter(Book.isbn == book_update.isbn, Book.id != book_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book with this ISBN already exists")

    update_data = book_update.model_dump(exclude_unset=True)
    return update_book(db, book, update_data)


@app.delete("/books/{book_id}")
def remove_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    delete_book(db, book)
    return {"message": "Book deleted successfully"}
