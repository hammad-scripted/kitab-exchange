from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from auth import verify_api_key
from database import get_session
from exceptions import BadRequestException, NotFoundException
from models.books import Book, BookCreate, BookResponse
from models.users import User

router = APIRouter(prefix="/books", tags=["books"])


@router.get(
    "/",
    response_model=list[BookResponse],
    description="List all unsold books with optional filters",
)
def list_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    query = select(Book).where(Book.is_sold == False)

    if title:
        query = query.where(Book.title.contains(title))
    if author:
        query = query.where(Book.author.contains(author))

    books = session.exec(query).all()
    if not books:
        raise NotFoundException("No available (unsold) books found matching your criteria")
    return books


@router.post("/", response_model=BookResponse, description="Create a new book listing")
def create_book(
    book: BookCreate,
    session: Session = Depends(get_session),
    _: str = Depends(verify_api_key),
):
    # Verify owner exists
    owner = session.get(User, book.user_id)
    if not owner:
        raise NotFoundException(f"Cannot create book: User with ID {book.user_id} does not exist")

    # Prevent duplicate titles
    existing_book = session.exec(
        select(Book).where(Book.title == book.title)
    ).first()
    if existing_book:
        raise BadRequestException(f"Book with title '{book.title}' already exists")

    new_book = Book.model_validate(book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


@router.get("/{book_id}", response_model=BookResponse, description="Get a book by ID")
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise NotFoundException(f"Book with ID {book_id} not found")
    return book