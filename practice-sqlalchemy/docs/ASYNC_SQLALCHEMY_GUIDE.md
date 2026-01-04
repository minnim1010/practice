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

### 5.1 Creating Tables

This function initializes the database by creating all necessary tables.

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

### 5.2 Create (Adding Data)

This function shows how to add a new record to the database.

```python
# main.py
from .database import AsyncSessionLocal
from .models import User

async def add_user(name: str, email: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_user = User(name=name, email=email)
            session.add(new_user)
            print(f"Added user: {name}")
```

### 5.3 Read (Querying Data)

This function retrieves records from the database.

```python
# main.py
from sqlalchemy.future import select

async def get_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        for user in users:
            print(f"Found user: id={user.id}, name={user.name}, email={user.email}")
        return users
```

### 5.4 Update (Updating Data)

To update an existing record, you first need to query it, modify its attributes, and then commit the session.

```python
# main.py

async def update_user_email(user_id: int, new_email: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Select the user to update
            result = await session.execute(select(User).filter(User.id == user_id))
            user_to_update = result.scalar_one_or_none()

            if user_to_update:
                user_to_update.email = new_email
                print(f"Updated user {user_id}'s email to {new_email}")
            else:
                print(f"User with id {user_id} not found.")
```

### 5.5 Delete (Deleting Data)

To delete a record, query it first, and then use `session.delete()` to mark it for deletion.

```python
# main.py

async def delete_user(user_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Select the user to delete
            result = await session.execute(select(User).filter(User.id == user_id))
            user_to_delete = result.scalar_one_or_none()

            if user_to_delete:
                await session.delete(user_to_delete)
                print(f"Deleted user with id {user_id}")
            else:
                print(f"User with id {user_id} not found.")
```

## 6. Running the Complete Example

Here is a complete example of how to run all the CRUD operations.

```python
# main.py
import asyncio
from .database import engine, Base, AsyncSessionLocal
from .models import User
from sqlalchemy.future import select

# ... (all the functions from section 5 should be defined here)

async def main():
    # Create tables
    await create_tables()

    # Add two users
    await add_user(name="Alice", email="alice@example.com")
    await add_user(name="Bob", email="bob@example.com")

    # Get and print all users
    print("\n--- Users after adding ---")
    users = await get_users()

    # Update Alice's email
    if users:
        alice_id = users[0].id
        await update_user_email(user_id=alice_id, new_email="alice.new@example.com")

    # Get and print users again to see the update
    print("\n--- Users after update ---")
    await get_users()

    # Delete Bob
    if len(users) > 1:
        bob_id = users[1].id
        await delete_user(user_id=bob_id)

    # Final list of users
    print("\n--- Users after deletion ---")
    await get_users()


if __name__ == "__main__":
    asyncio.run(main())
```

## 7. Handling Relationships

When working with relationships in async SQLAlchemy, it's crucial to manage how related objects are loaded to avoid performance issues.

### 7.1 Defining Models with Relationships

Let's define a one-to-many relationship between `User` and a new `Post` model. A user can have multiple posts.

```python
# src/app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    # By default, this relationship uses lazy='select', which is problematic in async.
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    # By default, this relationship uses lazy='select'.
    author = relationship("User", back_populates="posts")
```

### 7.2 Understanding Loading Strategies

In async code, **lazy loading is a major pitfall**. It issues a synchronous SQL query when a related attribute is first accessed, blocking the event loop. To prevent this, you must use **eager loading** strategies.

It's a strong recommendation to set `lazy='raise_on_sql'` on all relationships to prevent accidental lazy loads. This will raise a `DetachedInstanceError` if your code attempts a lazy load, making the problem immediately obvious.

```python
# In User model
posts = relationship("Post", back_populates="author", cascade="all, delete-orphan", lazy="raise_on_sql")

# In Post model
author = relationship("User", back_populates="posts", lazy="raise_on_sql")
```

Here are the primary eager loading strategies:

#### 7.2.1 `selectinload`

This is the most common and recommended strategy for one-to-many or many-to-many relationships.

- **How it works**: It issues a second `SELECT` statement that fetches all related objects for all the parent objects loaded in the initial query. It uses an `IN` clause with the primary keys of the parent objects.
- **Pros**: Avoids complex `JOIN`s and Cartesian products, which can be inefficient for "to-many" relationships. It results in predictable queries.
- **Cons**: Requires two separate queries.

```python
from sqlalchemy.orm import selectinload

# Correctly loads users and their posts in two separate queries
stmt = select(User).options(selectinload(User.posts))
result = await session.execute(stmt)
users = result.scalars().unique().all()
```

#### 7.2.2 `joinedload`

This strategy is typically used for many-to-one or one-to-one relationships.

- **How it works**: It uses a `LEFT OUTER JOIN` to fetch the parent and related objects in a single query.
- **Pros**: Fetches all data in one query, which can be faster for "to-one" relationships.
- **Cons**: For "to-many" relationships, it can create a Cartesian product, leading to a large amount of redundant data being transferred and processed by Python, which is inefficient. **Do not use `joinedload` for one-to-many relationships if the parent collection is large.**

```python
from sqlalchemy.orm import joinedload

# Correctly loads a post and its author in a single query
stmt = select(Post).options(joinedload(Post.author))
result = await session.execute(stmt)
posts = result.scalars().all()
```

#### 7.2.3 `subqueryload`

This is an alternative to `joinedload` for "to-many" relationships, but it's often more complex than `selectinload`.

- **How it works**: It issues a second query that `JOIN`s the parent and child tables, but it wraps the parent query in a subquery. This avoids the Cartesian product issue of `joinedload` in the main query.
- **Pros**: Can be more efficient than `joinedload` for "to-many" relationships in some specific database-dependent scenarios.
- **Cons**: The resulting query is more complex. `selectinload` is usually a better and simpler choice.

```python
from sqlalchemy.orm import subqueryload

stmt = select(User).options(subqueryload(User.posts))
result = await session.execute(stmt)
users = result.scalars().unique().all()
```

### 7.3 Creating and Querying with Relationships

When creating objects, you can build the relationship in memory before committing.

```python
# main.py

async def add_user_with_posts():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = User(name="Charlie", email="charlie@example.com")
            user.posts.append(Post(title="First Post", content="Hello World!"))
            user.posts.append(Post(title="Second Post", content="Async is fun!"))
            session.add(user)
            print("Added user Charlie with two posts")
```

When querying, always use an eager loading option like `selectinload`.

```python
# main.py
from sqlalchemy.orm import selectinload

async def get_users_with_posts_correctly():
    async with AsyncSessionLocal() as session:
        # Eagerly load the 'posts' relationship using selectinload
        result = await session.execute(
            select(User).options(selectinload(User.posts))
        )
        users = result.scalars().unique().all()

        for user in users:
            print(f"User: {user.name}")
            # Accessing user.posts will not trigger a new query
            for post in user.posts:
                print(f"  - Post: {post.title}")
        return users
```

### 7.4 Bad Code Example: Accidental Lazy Loading

Here is an example of what **not** to do. This code fetches users without eagerly loading their posts. When `user.posts` is accessed inside the loop, SQLAlchemy issues a new synchronous query for each user, causing the "N+1 problem" and blocking the event loop.

If `lazy='raise_on_sql'` is set on the relationship, this code will raise an error. If not, it will run with very poor performance.

```python
# main.py (BAD EXAMPLE - DO NOT USE)

async def get_users_with_posts_incorrectly():
    async with AsyncSessionLocal() as session:
        # This query does NOT eagerly load the posts.
        result = await session.execute(select(User))
        users = result.scalars().all()

        print("\n--- Incorrectly fetching posts (triggers lazy loading) ---")
        for user in users:
            print(f"User: {user.name}")
            try:
                # This access triggers a synchronous, blocking I/O call for each user.
                # This is the N+1 problem.
                for post in user.posts:
                    print(f"  - Post: {post.title}")
            except Exception as e:
                print(f"  - Error accessing posts: {e}")
                print("  - This error is expected if lazy='raise_on_sql' is set.")

```

### 7.5 Key Takeaways for Loading Strategies in Async

1.  **Always Use Eager Loading**: Lazy loading is not compatible with async code.
2.  **Set `lazy='raise_on_sql'`**: This is your safety net. It turns silent performance killers into loud errors during development.
3.  **Choose the Right Strategy**:
    - **`selectinload`**: Best for one-to-many and many-to-many relationships.
    - **`joinedload`**: Best for many-to-one and one-to-one relationships. Avoid for "to-many" collections.
4.  **Filter on Relationships**: When filtering based on attributes of a related model, you must use a `join()` or `outerjoin()` in your query, even if you are also using an eager loading option. The loading option controls what is loaded, while the `join` controls what is available for the `WHERE` clause.
    ```python
    # Find users who have posts with a specific title, and load all their posts
    stmt = (
        select(User)
        .join(User.posts)
        .filter(Post.title == "Async is fun!")
        .options(selectinload(User.posts))
    )
    ```
5.  **Use `.unique()`**: When using `selectinload` or `subqueryload`, you might get duplicate parent objects in the result set before they are fully processed. Always use `result.scalars().unique().all()` to get a list of unique parent instances.
