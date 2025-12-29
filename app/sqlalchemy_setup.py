from sqlalchemy import create_engine
# Import create_engine to connect SQLAlchemy to a database

from sqlalchemy.orm import sessionmaker, declarative_base
# sessionmaker → creates database sessions
# declarative_base → base class for ORM models

from .confic import settings
# Import settings from config file


# ======================
# DATABASE URL
# ======================

DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# Database connection URL
# Format: dialect+driver://username:password@host/database
# NOTE: Storing passwords in code is risky, use environment variables in production

# ======================
# ENGINE
# ======================

engine = create_engine(
    DATABASE_URL,
    echo=True  # set False in production
)
# Create SQLAlchemy engine to manage DB connections
# echo=True → prints all SQL queries (helpful for debugging)
# NOTE: Turn off echo in production for performance and security

# ======================
# SESSION
# ======================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# sessionmaker factory to create DB sessions
# autocommit=False → changes are not auto-saved, must call db.commit()
# autoflush=False → disables automatic flush before queries
# bind=engine → links session to the engine

# ======================
# BASE (for ORM models)
# ======================

Base = declarative_base()
# Base class for all ORM models
# Your models will inherit from Base
# NOTE: Required for SQLAlchemy ORM mapping

# ======================
# get db
# ======================

def get_db():
    # Dependency to get DB session in FastAPI
    db = SessionLocal()
    # Create a new session
    try:
        yield db
        # yield makes this a generator, usable with FastAPI Depends
    finally:
        db.close()
        # Close the session when done
        # NOTE: Always close sessions to avoid connection leaks
