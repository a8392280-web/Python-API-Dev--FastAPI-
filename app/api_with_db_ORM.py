from fastapi import FastAPI
from fastapi import Depends
# Import Depends to use dependency injection in FastAPI
# NOTE: This is how we inject the database session into routes

from sqlalchemy.orm import Session
# Import Session class to type hint DB sessions

from . import models
# Import your ORM models (Post, etc.)

from .sqlalchemy_setup import engine, get_db
# Import engine to create tables
# get_db → dependency function to get DB sessions


from .routers import post, users, auth, votes
# Import routers for posts and users

# ----------------------------------------------
# we are no more creating tables this way as we are using alembic for migrations
#models.Base.metadata.create_all(bind=engine) 
# Create all tables in the database based on models
# NOTE: Only creates tables if they don’t exist already
# WARNING: This does NOT update existing tables automatically

from fastapi.middleware.cors import CORSMiddleware
# Import CORS middleware to handle cross-origin requests
# NOTE: Useful when frontend and backend are on different domains/ports


app = FastAPI()
# Create a FastAPI application instance

# Configure CORS settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(votes.router)


# Include the post and user routers in the main app


# ----------------------------------------------

@app.get("/sqlalchemy")
# Define a GET route at /sqlalchemy

def test(db: Session = Depends(get_db)):
    # db is a SQLAlchemy session injected using Depends
    # NOTE: FastAPI automatically opens and closes the session

    return {"status": "success"}
    # Return a simple success response


@app.get("/") 
def root():
    return {"message": "Hello World"}
