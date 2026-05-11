# Message Persistence Service

A Python backend service for persisting AI assistant messages in a PostgreSQL database.

This project was implemented as a solution for a Python Backend Engineer assignment. The service exposes a REST API, stores messages in Postgres, secures endpoints with Bearer token authentication, and can be started with Docker Compose.

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker / Docker Compose
- Pydantic

## Features

- Create new messages
- Update existing messages
- Retrieve all messages
- Bearer token authentication for protected endpoints
- PostgreSQL persistence
- Dockerized application setup

## Message Schema

Messages follow this structure:

```json
{
  "message_id": "UUID4",
  "chat_id": "UUID4",
  "content": "string",
  "rating": true,
  "sent_at": "datetime",
  "role": "ai | user"
}
```

This schema matches the assignment requirements.

## Project Structure

```text
app/
  api/
    messages.py
  core/
    config.py
    security.py
  db/
    base.py
    models.py
    session.py
  schemas/
    message.py
  main.py

Dockerfile
docker-compose.yml
requirements.txt
.env.example
README.md
```

## Running the Project

### 1. Clone the repository

```bash
git clone <your-public-repo-url>
cd <repo-folder>
```

### 2. Create environment file

Copy `.env.example` to `.env` and provide your local values.

Example:

```env
API_TOKEN=your-secret-token
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/messages_db
```

### 3. Start the application

```bash
docker compose up --build
```

The API will be available at:

- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

The application and PostgreSQL database are started together with Docker Compose, as required by the assignment.


### 4. Stop the application
To stop the running containers:

```bash
docker compose down
```

## Authentication

All message endpoints are protected with Bearer token authentication.

Use the following header format:

```http
Authorization: Bearer your-secret-token
```

In Swagger UI, click **Authorize** and enter the same token value that you placed in your `.env` file.

## API Endpoints

### `POST /messages`

Create a new message.

Example request body:

```json
{
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "chat_id": "123e4567-e89b-42d3-a456-426614174000",
  "content": "Hello, this is a user message.",
  "rating": true,
  "sent_at": "2026-05-09T15:00:00Z",
  "role": "user"
}
```

### `GET /messages`

Return all persisted messages.

### `PATCH /messages/{message_id}`

Partially update an existing message.

Example request body:

```json
{
  "content": "Updated message content.",
  "rating": false
}
```

## Design Decisions

### Why FastAPI
FastAPI was chosen because it provides:
- simple REST API development
- automatic request validation with Pydantic
- automatic OpenAPI/Swagger documentation
- clean integration with dependency injection and SQLAlchemy

### Why Bearer token authentication
The assignment requires secured endpoints but does not prescribe a specific authentication mechanism. For this reason, a simple Bearer token approach was implemented as a lightweight and appropriate solution for the scope of the task.

### Why PATCH for updates
The update endpoint was implemented as `PATCH` because the service supports partial updates of existing messages. This better matches the actual behavior of the endpoint than a full resource replacement approach.

## Notes

- The application does not include a UI, as the assignment explicitly states that a UI is not required.
- Django was not used, in accordance with the assignment constraints.


## Future Improvements

If extended further, the following could be added:
- automated tests
- Alembic database migrations
- request logging
- healthcheck endpoint improvements
- filtering and pagination for `GET /messages`

## Assignment Reference

The implementation is based on the assignment requirements:
- Python service
- REST API
- PostgreSQL integration
- secured endpoints
- Docker Compose support
- public GitHub repository