from fastapi import APIRouter, Request, Depends, Query
from typing import Optional
from sqlmodel import SQLModel, Field, Query
from models.books import Book, BookCreate, BookResponse
from database import get_session
from sqlmodel import Session, select
from auth import verify_api_key
from exceptions import NotFoundException, BadRequestException, InternalServerException

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookResponse])
def list_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    session: Session = Depends(get_session),
    description="List all books in the database and filter by title and author if specified",
):
    query = select(Book).where(Book.is_sold == False)
    if not query:
        raise NotFoundException("No books found which are not sold")

    if title:
        query = query.where(Book.title == title)
    if author:
        query = query.where(Book.author == author)

    books = session.exec(query).all()
    if not books:
        raise NotFoundException("No books found")
    return books


@router.post("/", response_model=BookResponse)
def create_book(
    book: BookCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    # make sure api key is valid
    if api_key != "my_api_key":
        raise BadRequestException("Invalid API key")

    # make sure the book doesn't already exist
    existing_book = session.exec(select(Book).where(Book.title == book.title)).first()
    if existing_book:
        raise BadRequestException("Book with this title already exists")

    new_book = Book.model_validate(book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book
