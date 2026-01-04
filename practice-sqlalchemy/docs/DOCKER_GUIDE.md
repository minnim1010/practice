# Docker Guide for Python Projects

This guide explains how to use Docker to containerize a Python application.

## 1. What is Docker?

Docker is a platform that enables you to develop, ship, and run applications in isolated environments called containers. Containers bundle the application's code, runtime, and system dependencies, ensuring that the application runs consistently across different environments.

## 2. Creating a `Dockerfile`

A `Dockerfile` is a text file that contains instructions for building a Docker image. Create a file named `Dockerfile` in your project root.

Here is a sample `Dockerfile` for a Python application using `uv`:

```dockerfile
# Dockerfile

# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Install uv
RUN pip install uv

# 4. Copy the dependency files
COPY pyproject.toml uv.lock* ./

# 5. Install dependencies using uv
# First, install only dependencies to leverage Docker layer caching
RUN uv pip install --system --locked -e .

# 6. Copy the rest of the application's source code
COPY src/ ./src/

# 7. Expose the port the app runs on
EXPOSE 8000

# 8. Define the command to run the application
# This example assumes you are running a FastAPI app with uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 3. Creating a `.dockerignore` file

To speed up the build process and keep the image size small, exclude unnecessary files and directories by creating a `.dockerignore` file in your project root.

```
# .dockerignore

__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
.venv/
.git/
.pytest_cache/
.dockerignore
Dockerfile
```

## 4. Building the Docker Image

To build the Docker image, run the `docker build` command from your project root.

```bash
docker build -t my-python-app .
```
- `-t my-python-app`: Tags the image with the name `my-python-app`.
- `.`: Specifies the build context (the current directory).

## 5. Running the Docker Container

Once the image is built, you can run it as a container.

```bash
docker run -p 8000:8000 my-python-app
```
- `-p 8000:8000`: Maps port 8000 of the container to port 8000 on your local machine.

## 6. Using Docker Compose

For multi-container applications (e.g., an application and a database), `Docker Compose` is a convenient tool. Create a `docker-compose.yml` file in your project root.

Here is an example that runs the Python application and a PostgreSQL database.

```yaml
# docker-compose.yml

version: '3.8'

services:
  # Application service
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      # Ensure the app connects to the 'db' service
      DATABASE_URL: "postgresql+asyncpg://user:password@db/mydatabase"
    depends_on:
      - db

  # Database service
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydatabase
    volumes:
      - postgres_data:/var/lib/postgresql/data/

volumes:
  postgres_data:
```

### Running with Docker Compose

To start the services, run:
```bash
docker-compose up --build
docker-compose up --build -d # run in the background
```

To stop the services, run:
```bash
docker-compose down
```

## 7. Managing Docker Objects

Here are some common commands for managing Docker images, containers, and volumes.

### Images

- **List all images:**
  ```bash
  docker images
  ```

- **Remove a specific image:**
  ```bash
  docker rmi <image_id_or_name>
  ```

- **Remove all unused (dangling) images:**
  ```bash
  docker image prune
  ```

### Containers

- **List all running containers:**
  ```bash
  docker ps
  ```

- **List all containers (running and stopped):**
  ```bash
  docker ps -a
  ```

- **Stop a running container:**
  ```bash
  docker stop <container_id_or_name>
  ```

- **Start a stopped container:**
  ```bash
  docker start <container_id_or_name>
  ```

- **Remove a stopped container:**
  ```bash
  docker rm <container_id_or_name>
  ```

- **View logs from a container:**
  ```bash
  docker logs <container_id_or_name>
  ```
  - Use `-f` to follow the log output: `docker logs -f <container_id>`

- **Execute a command in a running container:**
  (e.g., open a shell)
  ```bash
  docker exec -it <container_id_or_name> /bin/bash
  ```

### System-wide Cleanup

- **Remove all stopped containers, unused networks, and dangling images:**
  ```bash
  docker system prune
  ```

- **Remove all stopped containers, unused networks, dangling images, and also unused volumes:**
  (Use with caution, as this will delete data in named volumes if they are not used by any container)
  ```bash
  docker system prune -a --volumes
  ```
