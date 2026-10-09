from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import Book, Category


def create_category(db: Session, name: str) -> Category:
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session) -> List[Category]:
    return db.query(Category).all()


def get_category_by_id(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()


def create_book(db: Session, book_data: dict) -> Book:
    book = Book(**book_data)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(db: Session) -> List[Book]:
    return db.query(Book).all()


def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db: Session, book: Book, update_data: dict) -> Book:
    for key, value in update_data.items():
        if value is not None:
            setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
