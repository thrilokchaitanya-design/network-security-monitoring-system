from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Capstone Backend is running!"


def test_invalid_login():
    response = client.post(
        "/auth/login",
        json={
            "username": "invalid_user",
            "password": "wrong_password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_viewer_login():
    response = client.post(
        "/auth/login",
        json={
            "username": "Thrilok",
            "password": "Thrilok@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_admin_login():
    response = client.post(
        "/auth/login",
        json={
            "username": "admin_test",
            "password": "Admin@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"