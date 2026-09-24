

from sqlalchemy import inspect, text
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///books.db"
engine = create_engine(DATABASE_URL, echo=True)


def create_tables():
    """
    Create all tables in the engine. This is equivalent to "create table" statements in raw SQL.
    """
    SQLModel.metadata.create_all(engine)

    # create_all() does not update indexes on tables that already exist. Add a
    # unique email index when opening databases created before the constraint
    # was introduced.
    email_indexes = inspect(engine).get_indexes("users")
    has_unique_email_index = any(
        index.get("column_names") == ["email"] and index.get("unique")
        for index in email_indexes
    )
    if not has_unique_email_index:
        with engine.begin() as connection:
            connection.execute(
                text("CREATE UNIQUE INDEX ux_users_email ON users (email)")
            )


def get_session():
    """Provide a transactional scope around a series of operations."""
    with Session(engine) as session:
        yield session
