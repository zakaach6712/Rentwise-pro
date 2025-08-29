# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional

# Database URL
ENGINE_URL = "sqlite:///rentwise.db"

# Globals to hold singletons
_engine: Optional[object] = None
_SessionLocal: Optional[sessionmaker] = None


def get_engine():
    """Return a singleton SQLAlchemy engine."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            ENGINE_URL,
            echo=False,      # Set True for SQL echo during debugging
            future=True
        )
    return _engine


def get_session():
    """
    Return a new SQLAlchemy Session.
    """
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            bind=get_engine(),
            autoflush=False,
            autocommit=False
        )
    return _SessionLocal()


def init_db() -> None:
    """
    Import all model modules so that they register themselves
    with SQLAlchemy's metadata, then create the tables.
    """
    from models import Base
    # Explicit imports so Base.metadata knows about all tables
    from models import property  # noqa: F401
    from models import tenant    # noqa: F401
    from models import lease     # noqa: F401
    from models import payment   # noqa: F401

    engine = get_engine()
    Base.metadata.create_all(engine)
