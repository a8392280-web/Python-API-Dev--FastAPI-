import psycopg # libirary  to connect Python to a PostgreSQL database
from fastapi import FastAPI
from fastapi.params import Body
from random import randrange
from fastapi import Response
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import status
try:
    conn = psycopg.connect(
        dbname="fastapi",
        user="postgres",
        password="123321123321",
        host="localhost",
        
    )
    cursor = conn.cursor()
    print("Connected successfully!")
except:
    print("failed")


app = FastAPI()


@app.get("/") 
def root():
    return {"message": "Hello World"}


# ----------------------------------------------

class Post(BaseModel):

    title: str

    content: str

    published: bool = True


# ----------------------------------------------

@app.get("/posts")

def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)

    return {"data": posts}
 


# ----------------------------------------------
 
@app.post("/posts", status_code=201)
def create_posts(post: Post):

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """ 
                   , (post.title, post.content, post.published))
    new_post= cursor.fetchone()
    conn.commit()

    return {"data": new_post}


# ----------------------------------------------

@app.get("/posts/{id}")
def get_post(id: str):

    cursor.execute("""SELECT * FROM posts WHERE id = %s""" ,(str(id),))
    post = cursor.fetchone()
 

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Post with ID {id} not found"
        )

    return {"post_detail": post}


# ----------------------------------------------



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:str):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""" ,(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()


    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ----------------------------------------------
@app.put("/posts/{id}")

def update_post(id: str, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content= %s, published=%s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id),))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )

    return {"data": updated_post}
