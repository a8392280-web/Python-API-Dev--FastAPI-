# 🧪 Alembic (Database Migrations for FastAPI / SQLAlchemy)

## 🔹 What is Alembic?
    # Alembic is a database migration tool for Python.
    # It helps manage changes to database schemas safely over time.

# Think of Alembic as:
# → Git, but for database structure (tables, columns, indexes)

# ---

## 🔹 Why Alembic is important
# Without Alembic:
    # - Manual SQL changes
    # - Risk of losing data
    # - Hard to track DB history

# With Alembic:
    # - Versioned schema changes
    # - Safe upgrades & downgrades
    # - Works perfectly with SQLAlchemy
    # - Required for production apps

# ---

## 🔹 Where Alembic is used
    # - FastAPI + SQLAlchemy
    # - Flask + SQLAlchemy
    # - PostgreSQL / MySQL / SQLite

# ---

## 🔹 Key Concepts

## 1️⃣ Migration
# A migration is a Python file that:
    # - Applies DB changes (upgrade)
    # - Reverts DB changes (downgrade)

# Example:
    # ```python
    # def upgrade():
    #     op.add_column("users", sa.Column("age", sa.Integer()))

    # def downgrade():
    #     op.drop_column("users", "age")
