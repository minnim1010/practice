# PostgreSQL Initial Setup Guide

This document provides instructions for setting up the initial PostgreSQL database, including creating a database, a user, and granting privileges.

## 1. Connect to PostgreSQL
First, connect to the PostgreSQL server.

### Default Connection
If you are connecting from the same machine where PostgreSQL is installed, you can connect as the `postgres` user.
```bash
psql -U postgres
```

### Connecting with a different Host, Port, or User
If your database is on a different server, or you need to specify a different port or user, use the following flags:
- `-h` or `--host`: The hostname of the database server.
- `-p` or `--port`: The port number the database server is listening on (default is 5432).
- `-U` or `--username`: The username to connect as.
- `-d` or `--dbname`: The database to connect to (optional).

Example:
```bash
psql -h your_host -p your_port -U your_username -d your_database
```
For example, to connect to a database on host `db.example.com` at port `5433` as user `myuser` to the `myapp` database, you would run:
```bash
psql -h db.example.com -p 5433 -U myuser -d myapp
```
You will be prompted for the user's password.

## 2. Create a Database
Create a new database for the application.

```sql
CREATE DATABASE myapp;
```

## 3. Create a User
Create a new user (role) that the application will use to connect to the database. Replace `password` with a strong password.

```sql
CREATE USER myuser WITH PASSWORD 'password';
```

## 4. Grant Privileges
Grant the necessary privileges to the new user on the new database.

```sql
GRANT ALL PRIVILEGES ON DATABASE myapp TO myuser;
```

### 4.1. Grant Privileges on a Schema (Optional)
If you are using a specific schema (e.g., `public`), you also need to grant usage on that schema.

```sql
-- Connect to the new database first
\c myapp

-- Grant usage on the schema
GRANT USAGE ON SCHEMA public TO myuser;

-- Grant privileges on all tables in the schema to the user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO myuser;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO myuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO myuser;
```

## 5. Create a Sample Table
Here is an example of how to create a sample table.

```sql
-- Make sure you are connected to the 'myapp' database
\c myapp

-- Create a sample table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO users (username, email) VALUES ('testuser', 'test@example.com');
```

## 6. Verify the Setup
You can verify that the user and table have been created correctly.

```sql
-- List databases
\l

-- List users
\du

-- Connect to the 'myapp' database as the new user
\c myapp myuser

-- List tables in the current database
\dt

-- Query the sample table
SELECT * FROM users;
```
