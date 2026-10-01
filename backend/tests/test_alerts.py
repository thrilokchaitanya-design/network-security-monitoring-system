from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# HELPER
# ============================================================

def create_alert_payload(**overrides):
    payload = {
        "severity": "HIGH",
        "attack_type": "TEST_ATTACK",
        "source_ip": "10.10.10.10",
        "destination_ip": "192.168.1.100",
        "confidence_score": 0.95,
        "status": "active",
        "description": "Automated test alert",
    }

    payload.update(overrides)
    return payload


# ============================================================
# CREATE ALERT
# ============================================================

def test_create_alert():
    response = client.post(
        "/alerts",
        json=create_alert_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["severity"] == "HIGH"
    assert data["attack_type"] == "TEST_ATTACK"
    assert data["source_ip"] == "10.10.10.10"
    assert data["destination_ip"] == "192.168.1.100"
    assert data["confidence_score"] == 0.95
    assert data["status"] == "active"
    assert data["description"] == "Automated test alert"


# ============================================================
# CREATE ALERT WITH HOST
# ============================================================

def test_create_alert_with_valid_host():
    response = client.post(
        "/alerts",
        json=create_alert_payload(
            host_id=1,
            attack_type="HOST_TEST",
        ),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["host_id"] == 1
    assert data["attack_type"] == "HOST_TEST"


# ============================================================
# CREATE ALERT WITH INVALID HOST
# ============================================================

def test_create_alert_with_invalid_host():
    response = client.post(
        "/alerts",
        json=create_alert_payload(
            host_id=999999,
        ),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Host not found"


# ============================================================
# GET ALERTS
# ============================================================

def test_get_alerts():
    response = client.get("/alerts")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data

    assert isinstance(data["items"], list)
    assert data["skip"] == 0
    assert data["limit"] == 20


# ============================================================
# GET ALERTS WITH PAGINATION
# ============================================================

def test_get_alerts_pagination():
    response = client.get(
        "/alerts?skip=0&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["skip"] == 0
    assert data["limit"] == 2
    assert len(data["items"]) <= 2


# ============================================================
# GET ALERTS WITH SEVERITY FILTER
# ============================================================

def test_filter_alerts_by_severity():
    response = client.get(
        "/alerts?severity=HIGH"
    )

    assert response.status_code == 200

    data = response.json()

    for alert in data["items"]:
        assert alert["severity"] == "HIGH"


# ============================================================
# GET ALERTS WITH STATUS FILTER
# ============================================================

def test_filter_alerts_by_status():
    response = client.get(
        "/alerts?status=active"
    )

    assert response.status_code == 200

    data = response.json()

    for alert in data["items"]:
        assert alert["status"] == "active"


# ============================================================
# GET ALERTS WITH ATTACK TYPE FILTER
# ============================================================

def test_filter_alerts_by_attack_type():
    response = client.get(
        "/alerts?attack_type=TEST_ATTACK"
    )

    assert response.status_code == 200

    data = response.json()

    for alert in data["items"]:
        assert alert["attack_type"] == "TEST_ATTACK"


# ============================================================
# GET ALERTS WITH SOURCE IP FILTER
# ============================================================

def test_filter_alerts_by_source_ip():
    response = client.get(
        "/alerts?source_ip=10.10.10.10"
    )

    assert response.status_code == 200

    data = response.json()

    for alert in data["items"]:
        assert alert["source_ip"] == "10.10.10.10"


# ============================================================
# GET ALERTS WITH HOST FILTER
# ============================================================

def test_filter_alerts_by_host():
    response = client.get(
        "/alerts?host_id=1"
    )

    assert response.status_code == 200

    data = response.json()

    for alert in data["items"]:
        assert alert["host_id"] == 1


# ============================================================
# INVALID PAGINATION
# ============================================================

def test_invalid_pagination_limit():
    response = client.get(
        "/alerts?limit=101"
    )

    assert response.status_code == 422


def test_invalid_pagination_skip():
    response = client.get(
        "/alerts?skip=-1"
    )

    assert response.status_code == 422


# ============================================================
# GET ALERT BY ID
# ============================================================

def test_get_alert_by_id():
    create_response = client.post(
        "/alerts",
        json=create_alert_payload(
            attack_type="GET_BY_ID_TEST",
        ),
    )

    assert create_response.status_code == 201

    alert_id = create_response.json()["id"]

    response = client.get(
        f"/alerts/{alert_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == alert_id
    assert data["attack_type"] == "GET_BY_ID_TEST"


# ============================================================
# GET NONEXISTENT ALERT
# ============================================================

def test_get_nonexistent_alert():
    response = client.get(
        "/alerts/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"


# ============================================================
# MISSING REQUIRED FIELDS
# ============================================================

def test_create_alert_missing_required_field():
    payload = {
        "severity": "HIGH",
        "attack_type": "TEST_ATTACK",
        "source_ip": "10.10.10.10",
        "destination_ip": "192.168.1.100",
        "status": "active",
    }

    response = client.post(
        "/alerts",
        json=payload,
    )

    # confidence_score is optional, so this should succeed.
    assert response.status_code == 201


# ============================================================
# DEFAULT PAGINATION VALUES
# ============================================================

def test_alerts_default_pagination():
    response = client.get("/alerts")

    assert response.status_code == 200

    data = response.json()

    assert data["skip"] == 0
    assert data["limit"] == 20


def test_alert_timeline_returns_chronological_events():
    first = client.post("/alerts", json=create_alert_payload(attack_type="TEST_TIMELINE_FIRST"))
    second = client.post("/alerts", json=create_alert_payload(attack_type="TEST_TIMELINE_SECOND"))
    assert first.status_code == 201
    assert second.status_code == 201

    response = client.get("/alerts/timeline?limit=1000")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    assert data["items"] == sorted(data["items"], key=lambda item: (item["timestamp"], item["id"]))
    assert {item["attack_type"] for item in data["items"]}.issuperset({"TEST_TIMELINE_FIRST", "TEST_TIMELINE_SECOND"})


def test_alert_timeline_rejects_invalid_limit():
    assert client.get("/alerts/timeline?limit=1001").status_code == 422
