from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

# datbase table for the user


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    college: str = Field(index=True)
    books: list["Book"] = Relationship(back_populates="owner")


# avoid circular import

from models.books import Book

User.model_rebuild()


# request body for creating a user
class UserCreate(SQLModel):
    name: str
    email: str
    college: str


# response body for getting a user


class UserResponse(SQLModel):
    id: int
    name: str
    email: str
    college: str
