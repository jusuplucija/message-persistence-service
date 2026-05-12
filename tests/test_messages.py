from app.core.config import settings


def auth_headers():
    return {"Authorization": f"Bearer {settings.api_token}"}


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_message(client):
    payload = {
        "message_id": "550e8400-e29b-41d4-a716-446655440000",
        "chat_id": "123e4567-e89b-42d3-a456-426614174000",
        "content": "Hello, this is second user message.",
        "rating": True,
        "sent_at": "2026-05-12T15:00:00Z",
        "role": "user",
    }

    response = client.post("/messages", json=payload, headers=auth_headers())

    assert response.status_code == 201
    data = response.json()
    assert data["message_id"] == payload["message_id"]
    assert data["chat_id"] == payload["chat_id"]
    assert data["content"] == payload["content"]
    assert data["rating"] == payload["rating"]
    assert data["role"] == payload["role"]


def test_get_messages(client):
    payload = {
        "message_id": "660e8400-e29b-41d4-a716-446655440000",
        "chat_id": "223e4567-e89b-42d3-a456-426614174000",
        "content": "Stored message",
        "rating": False,
        "sent_at": "2026-05-12T15:01:00Z",
        "role": "ai",
    }

    client.post("/messages", json=payload, headers=auth_headers())
    response = client.get("/messages", headers=auth_headers())

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(message["message_id"] == payload["message_id"] for message in data)


def test_update_message(client):
    payload = {
        "message_id": "770e8400-e29b-41d4-a716-446655440000",
        "chat_id": "323e4567-e89b-42d3-a456-426614174000",
        "content": "Original content",
        "rating": True,
        "sent_at": "2026-05-12T17:00:00Z",
        "role": "user",
    }

    client.post("/messages", json=payload, headers=auth_headers())

    update_payload = {
        "content": "Updated content",
        "rating": False,
    }

    response = client.patch(
        f"/messages/{payload['message_id']}",
        json=update_payload,
        headers=auth_headers(),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated content"
    assert data["rating"] is False


def test_patch_updates_only_provided_fields(client):
    payload = {
        "message_id": "bb0e8400-e29b-41d4-a716-446655440000",
        "chat_id": "723e4567-e89b-42d3-a456-426614174000",
        "content": "Original content",
        "rating": True,
        "sent_at": "2026-05-09T22:00:00Z",
        "role": "user",
    }

    create_response = client.post("/messages", json=payload, headers=auth_headers())
    assert create_response.status_code == 201

    patch_payload = {
        "content": "Partially updated content"
    }

    patch_response = client.patch(
        f"/messages/{payload['message_id']}",
        json=patch_payload,
        headers=auth_headers(),
    )

    assert patch_response.status_code == 200
    data = patch_response.json()

    assert data["content"] == "Partially updated content"
    assert data["rating"] is True
    assert data["role"] == "user"
    assert data["chat_id"] == payload["chat_id"]
    assert data["sent_at"] == payload["sent_at"]




# FAILURE TESTOVI

def test_create_message_requires_auth(client):
    payload = {
        "message_id": "880e8400-e29b-41d4-a716-446655440000",
        "chat_id": "423e4567-e89b-42d3-a456-426614174000",
        "content": "Unauthorized message",
        "rating": True,
        "sent_at": "2026-05-09T18:00:00Z",
        "role": "user",
    }

    response = client.post("/messages", json=payload)

    assert response.status_code in (401, 403)



def test_create_message_duplicate_id_returns_409(client):
    payload = {
        "message_id": "990e8400-e29b-41d4-a716-446655440000",
        "chat_id": "523e4567-e89b-42d3-a456-426614174000",
        "content": "First message",
        "rating": True,
        "sent_at": "2026-05-13T19:00:00Z",
        "role": "user",
    }

    first_response = client.post("/messages", json=payload, headers=auth_headers())
    second_response = client.post("/messages", json=payload, headers=auth_headers())

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Message with this ID already exists"


def test_update_missing_message_returns_404(client):
    update_payload = {
        "content": "Updated content",
        "rating": False,
    }

    response = client.patch(
        "/messages/11111111-1111-4111-8111-111111111111",
        json=update_payload,
        headers=auth_headers(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"


def test_create_message_invalid_payload_returns_422(client):
    invalid_payload = {
        "message_id": "not-a-valid-uuid",
        "chat_id": "123e4567-e89b-42d3-a456-426614174000",
        "content": "Invalid message",
        "rating": True,
        "sent_at": "2026-05-09T20:00:00Z",
        "role": "user",
    }

    response = client.post("/messages", json=invalid_payload, headers=auth_headers())

    assert response.status_code == 422


def test_create_message_with_invalid_token_returns_401(client):
    payload = {
        "message_id": "aa0e8400-e29b-41d4-a716-446655440000",
        "chat_id": "623e4567-e89b-42d3-a456-426614174000",
        "content": "Invalid token test",
        "rating": True,
        "sent_at": "2026-05-09T21:00:00Z",
        "role": "user",
    }

    invalid_headers = {"Authorization": "Bearer wrong-token"}

    response = client.post("/messages", json=payload, headers=invalid_headers)

    assert response.status_code == 401


def test_create_message_invalid_sent_at_returns_422(client):
    payload = {
        "message_id": "cc0e8400-e29b-41d4-a716-446655440000",
        "chat_id": "823e4567-e89b-42d3-a456-426614174000",
        "content": "Invalid sent_at test",
        "rating": True,
        "sent_at": "not-a-timestamp",
        "role": "user",
    }

    response = client.post("/messages", json=payload, headers=auth_headers())

    assert response.status_code == 422


def test_create_message_invalid_role_returns_422(client):
    payload = {
        "message_id": "dd0e8400-e29b-41d4-a716-446655440000",
        "chat_id": "923e4567-e89b-42d3-a456-426614174000",
        "content": "Invalid role test",
        "rating": True,
        "sent_at": "2026-05-09T23:00:00Z",
        "role": "assistant",
    }

    response = client.post("/messages", json=payload, headers=auth_headers())

    assert response.status_code == 422