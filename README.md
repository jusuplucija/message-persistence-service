# Message Persistence Service

A Python backend service for persisting AI assistant messages in a PostgreSQL database.

This project was implemented as a solution for a Python Backend Engineer assignment. The service exposes a REST API, stores messages in PostgreSQL, secures endpoints with Bearer token authentication, includes automated API tests, and can be started with Docker Compose.

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
- Automated API tests with pytest


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

tests/
  conftest.py
  test_messages.py

Dockerfile
docker-compose.yml
requirements.txt
.env.example
README.md
pytest.ini
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
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/messages_db
```
When running through Docker Compose, the database host must be `db`, which is the name of the PostgreSQL service in the Compose network.

### 3. Start the application

```bash
docker compose up --build
```

After the containers start, the API is available at:

- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

The application and PostgreSQL database are started together with Docker Compose.

- '`http://localhost:8000/health` - health check endpoint.


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


## Running Tests

The project includes automated API tests built with `pytest`.

Run the tests from the project root with:

```bash
pytest -v
```

If needed, tests can also be started with:

```bash
python -m pytest -v
```

The tests use a separate test database to avoid interfering with application data.


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
  "sent_at": "2026-05-14T15:00:00Z",
  "role": "user"
}
```

**Success responses:**
- `201 Created` - message was successfully persisted

**Possible error responses:**
- `401 Unauthorized` - invalid or missing Bearer token
- `409 Conflict` - a message with the same `message_id` already exists
- `422 Unprocessable Entity` - request body validation failed
- `500 Internal Server Error` – database operation failed.


### `GET /messages`

Return all persisted messages.

**Success responses:**
- `200 OK` - messages retrieved successfully

**Possible error responses:**
- `401 Unauthorized` - invalid or missing Bearer token
- `500 Internal Server Error` – database operation failed.


### `PATCH /messages/{message_id}`

Partially update an existing message.

Example request body:

```json
{
  "content": "Updated message content.",
  "rating": false
}
```

**Success responses:**
- `200 OK` - message was successfully updated

**Possible error responses:**
- `401 Unauthorized` - invalid or missing Bearer token
- `404 Not Found` - message with the given `message_id` does not exist
- `422 Unprocessable Entity` - request body or path parameter validation failed
- `500 Internal Server Error` – database operation failed.


## Implementation Notes

- FastAPI was chosen for quick REST API development, request validation, and built-in OpenAPI documentation.
- Bearer token authentication was used as a simple way to secure endpoints for the scope of the assignment.
- `PATCH` was used for the update endpoint because the implementation supports partial updates.