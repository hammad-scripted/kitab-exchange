

from sqlmodel import SQLModel,create_engine, Session

DATABASE_URL = "sqlite:///books.db"
engine = create_engine(DATABASE_URL, echo=True)


def create_tables():
    """
    Create all tables in the engine. This is equivalent to "create table" statements in raw SQL.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """Provide a transactional scope around a series of operations."""
    with Session(engine) as session:
        yield session
