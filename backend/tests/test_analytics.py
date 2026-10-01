from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_security_summary():
    response = client.get("/analytics/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_alerts" in data
    assert "active_alerts" in data
    assert "resolved_alerts" in data
    assert "severity" in data
    assert "average_confidence" in data

    assert "critical" in data["severity"]
    assert "high" in data["severity"]
    assert "medium" in data["severity"]
    assert "low" in data["severity"]


def test_stats_compatibility_endpoint_matches_summary():
    stats = client.get("/stats")
    summary = client.get("/analytics/summary")

    assert stats.status_code == 200
    assert stats.json() == summary.json()


def test_attack_distribution():
    response = client.get("/analytics/attacks")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for item in data:
        assert "attack_type" in item
        assert "count" in item
        assert isinstance(item["count"], int)


def test_severity_distribution():
    response = client.get("/analytics/severity")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for item in data:
        assert "severity" in item
        assert "count" in item
        assert isinstance(item["count"], int)


def test_attack_sources():
    response = client.get("/analytics/sources")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) <= 10

    for item in data:
        assert "source_ip" in item
        assert "count" in item
        assert isinstance(item["count"], int)
