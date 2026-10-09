from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    stock_quantity: int = 0
    category_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    stock_quantity: Optional[int] = None
    category_id: Optional[int] = None


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    isbn: str
    stock_quantity: int
    category_id: int
