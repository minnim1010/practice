# Asynchronous SQLAlchemy Guide

This guide provides a basic introduction to using SQLAlchemy with Python's `asyncio`.

## 1. Introduction

SQLAlchemy 1.4 introduced support for asynchronous operations, allowing you to write non-blocking database code. This is particularly useful for web applications and other I/O-bound tasks.

The core components for async operations are:
- `create_async_engine`: To create an asynchronous engine.
- `AsyncSession`: For managing asynchronous database sessions.
- `AsyncConnection`: For lower-level asynchronous database connections.

## 2. Installation

First, you need to install SQLAlchemy and an async database driver. The driver depends on the database you are using.

- **For PostgreSQL:**
  ```bash
  uv pip install sqlalchemy "asyncpg"
  ```

- **For SQLite:**
  ```bash
  uv pip install sqlalchemy "aiosqlite"
  ```

- **For MySQL:**
  ```bash
  uv pip install sqlalchemy "aiomysql"
  ```

## 3. Setting up the Engine and Session

To interact with the database, you need to create an `AsyncEngine` and configure an `AsyncSession`.

```python
# src/app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Define the database URL
# For async PostgreSQL: "postgresql+asyncpg://user:password@host/dbname"
# For async SQLite: "sqlite+aiosqlite:///mydatabase.db"
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session maker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

# Base class for declarative models
Base = declarative_base()
```

## 4. Defining a Model

Define your models by inheriting from the `declarative_base`. This is the same as in synchronous SQLAlchemy.

```python
# src/app/models.py

from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

## 5. Performing CRUD Operations

Use `AsyncSession` within an `async` function to perform database operations. The `async with` block ensures the session is properly closed.

### Creating Tables

```python
# main.py
import asyncio
from .database import engine, Base
from .models import User

async def create_tables():
    async with engine.begin() as conn:
        # This will drop all tables and recreate them
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
```

### Adding Data

```python
# main.py
from .database import AsyncSessionLocal
from .models import User
from sqlalchemy.future import select

async def add_user(name: str, email: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_user = User(name=name, email=email)
            session.add(new_user)
            print(f"Added user: {name}")

async def get_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        for user in users:
            print(f"Found user: id={user.id}, name={user.name}, email={user.email}")
```

### Running the Example

Here is a complete example of how to run the async functions.

```python
# main.py
import asyncio
from .database import engine, Base, AsyncSessionLocal
from .models import User
from sqlalchemy.future import select

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def add_user(name: str, email: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_user = User(name=name, email=email)
            session.add(new_user)
            print(f"Added user: {name}")

async def get_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        for user in users:
            print(f"Found user: id={user.id}, name={user.name}, email={user.email}")

async def main():
    await create_tables()
    await add_user(name="Alice", email="alice@example.com")
    await add_user(name="Bob", email="bob@example.com")
    await get_users()

if __name__ == "__main__":
    asyncio.run(main())
```
