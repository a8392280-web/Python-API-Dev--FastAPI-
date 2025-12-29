# # What is ORM (Object-Relational Mapping)?

## Definition:

    # ORM (Object-Relational Mapping) is a technique that allows developers to interact
    # with a database using **programming language objects** instead of writing raw SQL
    # queries.

# ORM maps:
    # - Database tables → Python classes
    # - Table rows → Python objects
    # - Columns → Object attributes

# --------

## The Problem ORM Solves

    # Databases use **SQL**
    # Applications use **Python objects**

# Without ORM, you must:

    # - Write SQL manually
    # - Handle query parameters
    # - Convert tuples to usable data
    # - Repeat SQL everywhere

# ---

## Without ORM (Raw SQL Example)

"""
cursor.execute(
    "SELECT * FROM posts WHERE id = %s",
    (id,)
)
post = cursor.fetchone()
"""
# Problems:

    # Column order matters

    # Hard to maintain

    # Easy to make mistakes

## With ORM (Clean & Pythonic)

"""
post = db.query(Post).filter(Post.id == id).first()
"""

# No SQL required.

## ORM Model Example:

"""
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)

"""
# This class represents a database table.

## ORM CRUD Examples:

# Create
"""
post = Post(title="Hello", content="World")
db.add(post)
db.commit()
"""
# Read
"""
posts = db.query(Post).all()
"""
# Update
"""
post.title = "New Title"
db.commit()
"""

# Delete
"""
db.delete(post)
db.commit()
"""

## Popular Python ORM

# SQLAlchemy (Most Used)

    # Industry standard

    # Officially recommended by FastAPI

    # Used in production systems

"""
| Feature         | Raw SQL   | ORM  |
| --------------- | -------  | ---  |
| Ease of use     | ❌       | ✅   |
| Readability     | ❌       | ✅   |
| Maintainability | ❌       | ✅   |
| Security        | ⚠️       | ✅   |
| Performance     | ✅       | ⚠️   |
| Large projects  | ❌       | ✅   |
"""
## When to Use ORM

# Use ORM when:

    # Building APIs (FastAPI, Flask)

    # Doing CRUD operations

    # Working on long-term projects

    # Freelancing or production apps

# Use Raw SQL when:

    # Writing complex queries

    # High-performance reporting

    # Simple scripts