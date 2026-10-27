from fastapi.testclient import TestClient

from main import create_app


def test_register_endpoint():
    client = TestClient(create_app())

    response = client.post("/auth/register", json={"email": "ana@example.com", "password": "secreto123"})
    assert response.status_code == 201
    assert "id" in response.json()

    duplicated = client.post("/auth/register", json={"email": "ana@example.com", "password": "secreto123"})
    assert duplicated.status_code == 409

    invalid = client.post("/auth/register", json={"email": "nope", "password": "secreto123"})
    assert invalid.status_code == 422
