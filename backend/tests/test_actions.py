from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def login(username, password):
    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_admin_can_create_alert_action():
    token = login("admin_test", "Admin@123")

    response = client.post(
        "/alerts/1/actions",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "action": "ACKNOWLEDGED",
            "details": "Admin acknowledged the alert",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["alert_id"] == 1
    assert data["action"] == "ACKNOWLEDGED"
    assert data["performed_by"] == "admin_test"
    assert data["details"] == "Admin acknowledged the alert"


def test_invalid_action_is_rejected():
    token = login("admin_test", "Admin@123")

    response = client.post(
        "/alerts/1/actions",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "action": "INVALID_ACTION",
            "details": "This should fail",
        },
    )

    assert response.status_code == 400
    assert "Invalid action" in response.json()["detail"]


def test_action_requires_authentication():
    response = client.post(
        "/alerts/1/actions",
        json={
            "action": "ACKNOWLEDGED",
        },
    )

    assert response.status_code == 401


def test_action_for_nonexistent_alert():
    token = login("admin_test", "Admin@123")

    response = client.post(
        "/alerts/999999/actions",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "action": "ACKNOWLEDGED",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"


def test_admin_can_get_alert_actions():
    token = login("admin_test", "Admin@123")

    response = client.get(
        "/alerts/1/actions",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)