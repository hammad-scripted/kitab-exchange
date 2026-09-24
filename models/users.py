from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.books import Book


# Database table for the user
class User(SQLModel, table=True):
    __tablename__ = "users"  # Explicitly set the table name to "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    college: str = Field(index=True)
    books: list["Book"] = Relationship(back_populates="owner")


# Import Book (not User) to resolve Relationship forward reference
from models.books import Book

User.model_rebuild()


# Request body for creating a user
class UserCreate(SQLModel):
    name: str
    email: str
    college: str


# Response body for getting a user
class UserResponse(SQLModel):
    id: int
    name: str
    email: str
    college: str