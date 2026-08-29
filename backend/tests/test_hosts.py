from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# LOGIN HELPERS
# ============================================================

def get_viewer_headers():
    response = client.post(
        "/auth/login",
        json={
            "username": "Thrilok",
            "password": "Thrilok@123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def get_admin_headers():
    response = client.post(
        "/auth/login",
        json={
            "username": "admin_test",
            "password": "Admin@123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# ============================================================
# GET HOSTS
# ============================================================

def test_viewer_cannot_get_hosts():
    headers = get_viewer_headers()

    response = client.get(
        "/hosts",
        headers=headers,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"


def test_admin_can_get_hosts():
    headers = get_admin_headers()

    response = client.get(
        "/hosts",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# ============================================================
# CREATE HOST
# ============================================================

def test_viewer_cannot_create_host():
    headers = get_viewer_headers()

    response = client.post(
        "/hosts",
        headers=headers,
        json={
            "hostname": "pytest-viewer-host",
            "ip_address": "192.168.1.210",
            "mac_address": "00:1A:2B:3C:4D:10",
            "status": "online",
            "risk_score": 5.0,
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"


def test_admin_can_create_host():
    headers = get_admin_headers()

    response = client.post(
        "/hosts",
        headers=headers,
        json={
            "hostname": "pytest-admin-host",
            "ip_address": "192.168.1.211",
            "mac_address": "00:1A:2B:3C:4D:11",
            "status": "online",
            "risk_score": 10.0,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["hostname"] == "pytest-admin-host"
    assert data["ip_address"] == "192.168.1.211"
    assert data["mac_address"] == "00:1A:2B:3C:4D:11"
    assert data["status"] == "online"
    assert data["risk_score"] == 10.0

    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


# ============================================================
# DUPLICATE HOST VALIDATION
# ============================================================

def test_duplicate_hostname_is_rejected():
    headers = get_admin_headers()

    response = client.post(
        "/hosts",
        headers=headers,
        json={
            "hostname": "pytest-duplicate-host",
            "ip_address": "192.168.1.212",
            "mac_address": "00:1A:2B:3C:4D:12",
            "status": "online",
            "risk_score": 10.0,
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/hosts",
        headers=headers,
        json={
            "hostname": "pytest-duplicate-host",
            "ip_address": "192.168.1.213",
            "mac_address": "00:1A:2B:3C:4D:13",
            "status": "online",
            "risk_score": 20.0,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Hostname already exists"


def test_duplicate_ip_is_rejected():
    headers = get_admin_headers()

    response = client.post(
        "/hosts",
        headers=headers,
        json={
            "hostname": "pytest-ip-host",
            "ip_address": "192.168.1.214",
            "mac_address": "00:1A:2B:3C:4D:14",
            "status": "online",
            "risk_score": 10.0,
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/hosts",
        headers=headers,
        json={
            "hostname": "pytest-ip-host-duplicate",
            "ip_address": "192.168.1.214",
            "mac_address": "00:1A:2B:3C:4D:15",
            "status": "online",
            "risk_score": 20.0,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "IP address already exists"


def test_duplicate_mac_is_rejected():
    headers = get_admin_headers()

    response = client.post(
        "/hosts",
        headers=headers,
        json={
            "hostname": "pytest-mac-host",
            "ip_address": "192.168.1.215",
            "mac_address": "00:1A:2B:3C:4D:16",
            "status": "online",
            "risk_score": 10.0,
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/hosts",
        headers=headers,
        json={
            "hostname": "pytest-mac-host-duplicate",
            "ip_address": "192.168.1.216",
            "mac_address": "00:1A:2B:3C:4D:16",
            "status": "online",
            "risk_score": 20.0,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "MAC address already exists"


# ============================================================
# GET HOST BY ID
# ============================================================

def test_admin_can_get_host_by_id():
    headers = get_admin_headers()

    response = client.get(
        "/hosts/1",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert "hostname" in data
    assert "ip_address" in data
    assert "mac_address" in data


def test_get_nonexistent_host():
    headers = get_admin_headers()

    response = client.get(
        "/hosts/999999",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Host not found"


# ============================================================
# UPDATE HOST
# ============================================================

def test_viewer_cannot_update_host():
    headers = get_viewer_headers()

    response = client.patch(
        "/hosts/1",
        headers=headers,
        json={
            "risk_score": 99.0,
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"


def test_admin_can_update_host():
    headers = get_admin_headers()

    response = client.patch(
        "/hosts/1",
        headers=headers,
        json={
            "risk_score": 75.0,
            "status": "online",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["risk_score"] == 75.0
    assert data["status"] == "online"


# ============================================================
# HOST ALERTS
# ============================================================

def test_admin_can_get_host_alerts():
    headers = get_admin_headers()

    response = client.get(
        "/hosts/1/alerts",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_alerts_for_nonexistent_host():
    headers = get_admin_headers()

    response = client.get(
        "/hosts/999999/alerts",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Host not found"


# ============================================================
# SECURITY SUMMARY
# ============================================================

def test_admin_can_get_security_summary():
    headers = get_admin_headers()

    response = client.get(
        "/hosts/1/security-summary",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "host" in data
    assert "security" in data

    assert "id" in data["host"]
    assert "hostname" in data["host"]
    assert "ip_address" in data["host"]
    assert "risk_score" in data["host"]

    assert "total_alerts" in data["security"]
    assert "active_alerts" in data["security"]
    assert "resolved_alerts" in data["security"]
    assert "severity" in data["security"]
    assert "average_confidence" in data["security"]


def test_security_summary_for_nonexistent_host():
    headers = get_admin_headers()

    response = client.get(
        "/hosts/999999/security-summary",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Host not found"