# retwise_pro/init_db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

# Explicitly import all models to ensure they're registered with Base.metadata
from models.property import Property
from models.tenant import Tenant
from models.lease import Lease
from models.payment import Payment

# Allow DB URL to be overridden via environment variable
DB_URL = os.getenv("RENTWISE_DB_URL", "sqlite:///dev.db")

# Create a single reusable engine
engine = create_engine(
    DB_URL,
    echo=True,
    connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
)

# Thread‑safe session factory
SessionLocal = scoped_session(sessionmaker(bind=engine))

def init_db(drop_existing: bool = False) -> None:
    """
    Initialize the database schema.
    Set drop_existing=True to drop and recreate tables (dev use only).
    """
    if drop_existing:
        print("Dropping all tables...")
        Base.metadata.drop_all(engine)
    print("Creating all tables...")
    Base.metadata.create_all(engine)
    print(" Database tables created successfully!")

if __name__ == "__main__":
    # Pass drop_existing=True here if you
    init_db()