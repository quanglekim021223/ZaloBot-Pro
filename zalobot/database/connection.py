"""Database configuration and session management"""
from sqlmodel import SQLModel, create_engine, Session

# SQLite database file
DATABASE_URL = "sqlite:///zalobot.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    """Initialize database - create all tables"""
    # Import models here to ensure they're registered with SQLModel
    from zalobot.database.models import Order  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency for FastAPI to get database session"""
    with Session(engine) as session:
        yield session

