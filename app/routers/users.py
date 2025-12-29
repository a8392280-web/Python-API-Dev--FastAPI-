from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from .. import models,utiles, schemas
from ..sqlalchemy_setup import get_db



router = APIRouter(
    prefix="/users", # Prefix for all routes in this router instead of writing ("/posts") for each route
    tags=["Users"] # Tagging the routes for documentation purposes
)


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate,db: Session = Depends(get_db)):

    # Hash the user's password before storing it
    hashed_password = utiles.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# ----------------------------------
@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):


    user = db.query(models.User).filter(models.User.id == id).first()
    # Query the User with the given ID
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {id} not found"
        )

    return user