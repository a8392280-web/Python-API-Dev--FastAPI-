from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship
# Import column types for SQLAlchemy ORM
# Column → defines a database column
# Integer, String, Boolean → types of the column

from .sqlalchemy_setup import Base
# Import the Base class from your setup
# All ORM models must inherit from Base

# every models = Table in Database
# NOTE: Each class becomes a table in the database

class Post(Base):
    # Define a new ORM model for posts
    # Inherits from Base

    __tablename__ = "posts"
    # Name of the database table
    # NOTE: Must be unique in the database

    id = Column(Integer, primary_key=True, index=True)
    # Primary key column of type Integer
    # index=True → creates an index for faster lookups

    title = Column(String, nullable=False)
    # Title column, must be a string and cannot be NULL
    # NOTE: nullable=False enforces data integrity

    content = Column(String, nullable=False)
    # Content column, string, cannot be NULL

    published = Column(Boolean, server_default=text("true"), nullable=False)
    # Boolean column to indicate if post is published
    # default=True → automatically set to True if not provided 

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Create relationship to between posts.owner_id and users.id (posts.owner_id = users.id)
    # Foreign key column referencing users table
    # ondelete="CASCADE" → if the referenced user is deleted, delete this post

    owner = relationship("User")
    # Establish relationship to User model
    # Allows access to the User object associated with this post




class User(Base):
    # Define a new ORM model for users
    # Inherits from Base

    __tablename__ = "users"
    # Name of the database table

    id = Column(Integer, primary_key=True, index=True)
    # Primary key column of type Integer

    email = Column(String, unique=True, nullable=False)
    # Email column, must be unique and cannot be NULL

    password = Column(String, nullable=False)
    # Password column, cannot be NULL

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    # Timestamp column for when the user was created


class Vote(Base):
    # Define a new ORM model for votes
    # Inherits from Base

    __tablename__ = "votes"
    # Name of the database table

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    # Foreign key column referencing users table
    # ondelete="CASCADE" → if the referenced user is deleted, delete this vote
    # primary_key=True → part of composite primary key

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    # Foreign key column referencing posts table
    # ondelete="CASCADE" → if the referenced post is deleted, delete this vote
    # primary_key=True → part of composite primary key