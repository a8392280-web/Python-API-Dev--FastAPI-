from fastapi import FastAPI
# Import the FastAPI class from the fastapi package
# This class is used to create your API application


# info: name of the fuction does not matter its only for readability.

app = FastAPI()
# Create an instance of the FastAPI app
# 'app' is the main object that will handle requests and responses

@app.get("/") 
# This is a DECORATOR
# It tells FastAPI:
# "When someone sends a GET request to the root URL /"

def root():
    # This is a function that runs when / is requested
    # The function name can be anything (root, home, index, etc.)

    return {"message": "Hello World"}
    # FastAPI automatically converts this Python dictionary to JSON
    # This is the response sent back to the client (browser, app, etc.)


@app.get("/movies")
def get_movies():
    # another example

    return {"movie":"the batman"}

# info: if there two rout(@app) , with the same HTTP Methode(.get) , with the same path("/") [@app.get("/") ]
    # the first one who is shows (because the code run form top to down and end if finds the function he wants )

# info: We use Postman to test out API


# ----------------------------------------------



from fastapi.params import Body
# Import Body to tell FastAPI that the data comes from the request body
# NOTE: `from fastapi import Body` is more common, but this still works

@app.post("/create")
# Define a POST route at the path /createpost

def create_post(payload: dict = Body(...)):
    # Create a route handler function
    # payload is expected to be a dictionary from the request body
    # Body(...) means the body is REQUIRED

    # NOTE: Using a Pydantic model is the recommended FastAPI way

    return {
        f"seccesfyly made a post Title: {payload['title']}, Content:{payload['content']}"
    }
    # Return a response to the client using values from the payload
    # NOTE: `{ "text" }` creates a SET, not a dictionary
    # NOTE: Accessing payload['title'] directly can raise KeyError if missing


# ----------------------------------------------

from pydantic import BaseModel
# Import BaseModel from Pydantic
# This is used to define and validate request data schemas

class Post(BaseModel):
    # Define a data model for a post
    # FastAPI uses this to validate incoming JSON automatically

    title: str
    # Title field, must be a string
    # NOTE: If the client does not send this, FastAPI returns an automatic error

    content: str
    # Content field, must be a string
    # NOTE: Type validation happens automatically (no manual checks needed)


@app.post("/createposts")
# Define a POST route at /createposts

def create_post(new_post: Post):
    # Route handler function
    # new_post is automatically created from the request body
    # FastAPI converts JSON → Post object

    print(new_post)
    # Prints the Post object representation
    # NOTE: This is mainly for debugging, not for production use

    print(new_post.title)
    # Access the title attribute from the Post object
    # NOTE: Dot notation is safer and cleaner than dictionary access

    print(new_post.content)
    # Access the content attribute from the Post object

    print(new_post.model_dump())
    # Convert the Post object into a dictionary
    # NOTE: model_dump() replaces .dict() in newer Pydantic versions

    return {"data": "new post"}
    # Return a simple response to the client
    # NOTE: You can return new_post.model_dump() to send back the created post


# ----------------------------------------------


from random import randrange
# Import randrange to generate random numbers for post IDs
# NOTE: Random IDs can collide; databases usually handle this better

from fastapi import Response
# Import Response to manually control HTTP response status codes

from fastapi import HTTPException
# Import HTTPException to raise proper HTTP errors

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2}
]
# In-memory list acting as a fake database
# NOTE: Data will reset every time the server restarts

@app.get("/posts")
# Define a GET route to fetch all posts

def get_posts():
    # Route handler that returns all posts
    return {"data": my_posts}
    # Return posts wrapped inside a dictionary

@app.post("/posts", status_code=201)
# Define a POST route to create a new post
# status_code=201 means "Created"

def create_posts(post: Post):
    # Receive a Post object from the request body
    # FastAPI validates it using the Post Pydantic model

    post_dict = post.model_dump()
    # Convert the Post object into a dictionary
    # NOTE: model_dump() is the modern Pydantic method

    post_dict['id'] = randrange(0, 10000)
    # Generate a random ID for the post
    # NOTE: No check for duplicate IDs

    my_posts.append(post_dict)
    # Add the new post to the in-memory list

    return {"data": post_dict}
    # Return the created post

def find_post(id):
    # Helper function to find a post by ID

    for p in my_posts:
        # Loop through all stored posts

        if p.get("id") == id:
            # Check if the current post ID matches
            return p
            # Return the matching post

@app.get("/posts/{id}")
# Define a GET route with a path parameter (id)

def get_post(id: int, response: Response):
    # id is taken from the URL and converted to int automatically
    # response allows manual control of HTTP status code

    post = find_post(id)
    # Try to find the post with the given ID

    if not post:
        # If no post was found


        raise HTTPException(
            status_code=404,
            detail=f"Post with ID {id} not found"
        )
        # Raise an HTTP error instead of returning a response
        # NOTE: This immediately stops the function execution


    return {"post_detail": post}
    # Return the found post


# ----------------------------------------------
from fastapi import status
# Import HTTP status codes from FastAPI
# NOTE: Using status constants improves readability

def find_index_post(id):
    # Helper function to find the index of a post by ID

    for i, p in enumerate(my_posts):
        # enumerate gives both index (i) and item (p)

        if p['id'] == int(id):
            # Check if the post ID matches the given ID
            # NOTE: Casting to int ensures correct comparison

            return i
            # Return the index of the matching post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# Define a DELETE route to remove a post by ID
# 204 means "No Content"

def delete_post(id):
    # Route handler for deleting a post

    index = find_index_post(id)
    # Find the index of the post to delete

    print(index)
    # Print index for debugging purposes
    # NOTE: Should be removed or replaced with logging in production

    if index == None:
        # If the post does not exist

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )
        # Raise a 404 error
        # NOTE: Raising HTTPException stops function execution

    my_posts.pop(index)
    # Remove the post from the list using its index

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # Return an empty response with 204 status
    # NOTE: When using status_code in decorator, returning Response is optional

@app.put("/posts/{id}")
# Define a PUT route to update a post by ID

def update_post(id: int, post: Post):
    # Route handler to update an existing post
    # id comes from the URL path
    # post comes from the request body

    index = find_index_post(int(id))
    # Find the index of the post to update


    print(index)
    # Print index for debugging
    # NOTE: Use logging instead of print in real projects

    if index == None:
        # If the post does not exist

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )
        # Raise a 404 error

    post_dict = post.model_dump()
    # Convert the Post object to a dictionary

    post_dict['id'] = int(id)
    # Ensure the ID remains the same as the URL parameter
    # NOTE: This prevents clients from changing the ID

    my_posts[index] = post_dict
    # Replace the old post with the updated one

    return {"data": post_dict}
    # Return the updated post
