from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from models.users import User


class Books(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: float = Field(index=True)
    is_sold: bool = Field(default=False)

    # foreign key to user table
    user_id:  = Field(default=None, foreign_key="users.id")
    owner: Optional["User"] = Relationship(back_populates="books")
    
# avoid circular import - a circular import is when two modules import each other
from models.users import User
Books.model_rebuild()

# request body for creating a book
class BookCreate(SQLModel):
    title: str
    author: str
    price: float
    user_id: int

# response body for getting a book
class BookResponse(SQLModel):
    id: int
    title: str
    author: str
    price: float
    is_sold: bool
    user_id: int
    
    