from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status     
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import oauth2
from .. import models, schemas
from ..sqlalchemy_setup import get_db

router = APIRouter(
    prefix="/posts", # Prefix for all routes in this router instead of writing ("/posts") for each route
    tags=["Posts"] # Tagging the routes for documentation purposes(you can see this in /docs)
)

# ----------------------------------------------
@router.get("/", response_model=List[schemas.PostOut])

def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit: int = 2, skip: int = 0,search: Optional[str] = ""):
    # post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # Query all Post records from the database

    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
                models.Post.id).filter(
                    models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return post
 


# ----------------------------------------------

@router.post("/", status_code=201,response_model=schemas.PostResp)
def create_posts(post: schemas.Post,db: Session = Depends(get_db) , get_current_user: int = Depends(oauth2.get_current_user)):
    # **post.model_dump(): gets all the data from pydantic model without writing each field like this:- title=post.title, content=post.content, published=post.published
    new_post = models.Post(owner_id=get_current_user.id, **post.model_dump()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
# ----------------------------------------------

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: str, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):


    # post = db.query(models.Post).filter(models.Post.id == int(id)).first()
    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
                models.Post.id).filter(models.Post.id == int(id)).first()
    
    # Query the Post with the given ID
    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Post with ID {id} not found"
        )

    # if  post[0].owner_id != get_current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to perform requested action"
    #     )

    return post


# # ----------------------------------------------



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:str, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == int(id)).first()
    

    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )
    if  post_query.owner_id != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    db.delete(post_query)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ----------------------------------------------
@router.put("/{id}",response_model=schemas.PostResp)

def update_post(id: str, post: schemas.Post, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    updated_post = db.query(models.Post).filter(models.Post.id == int(id))
    selected_post = updated_post.first()

    if selected_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )
    if  selected_post.owner_id != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()


    return updated_post.first()