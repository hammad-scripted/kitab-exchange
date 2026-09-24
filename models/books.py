from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: float = Field(index=True)
    is_sold: bool = Field(default=False)

    # Foreign key now correctly points to table "users"
    user_id: int = Field(default=None, foreign_key="users.id")
    owner: Optional["User"] = Relationship(back_populates="books")


# Import User to resolve Relationship forward reference
from models.users import User

Book.model_rebuild()


# Request body for creating a book
class BookCreate(SQLModel):
    title: str
    author: str
    price: float
    user_id: int


# Response body for getting a book
class BookResponse(SQLModel):
    id: int
    title: str
    author: str
    price: float
    is_sold: bool
    user_id: int