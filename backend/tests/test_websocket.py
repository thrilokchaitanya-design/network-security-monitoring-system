import asyncio

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_websocket_connection():
    with client.websocket_connect("/ws/alerts") as websocket:
        websocket.send_text("ping")


def test_websocket_receives_broadcast():
    async def run_test():
        from app.api.websocket import manager

        received = asyncio.Event()

        class FakeWebSocket:
            async def send_json(self, message):
                assert message["type"] == "alert"
                assert message["data"]["attack_type"] == "DDoS"
                received.set()

        fake = FakeWebSocket()

        manager.active_connections.append(fake)

        try:
            await manager.broadcast(
                {
                    "type": "alert",
                    "data": {
                        "id": 999,
                        "severity": "CRITICAL",
                        "attack_type": "DDoS",
                        "source_ip": "192.168.1.250",
                        "destination_ip": "192.168.1.1",
                    },
                }
            )

            await asyncio.wait_for(received.wait(), timeout=2)

        finally:
            manager.disconnect(fake)

    asyncio.run(run_test())


def test_websocket_disconnect():
    with client.websocket_connect("/ws/alerts") as websocket:
        websocket.send_text("test")

    assert True


def test_alert_ingestion_broadcasts_persisted_event():
    payload = {
        "severity": "HIGH",
        "attack_type": "TEST_WEBSOCKET_PIPELINE",
        "source_ip": "10.0.0.20",
        "destination_ip": "10.0.0.30",
        "confidence_score": 0.91,
        "status": "active",
        "description": "Integration path test",
    }

    with client.websocket_connect("/ws/alerts") as websocket:
        response = client.post("/alerts", json=payload)
        assert response.status_code == 201
        stored_alert = response.json()
        message = websocket.receive_json()

    assert message["type"] == "alert"
    assert message["data"]["id"] == stored_alert["id"]
    assert message["data"]["attack_type"] == payload["attack_type"]
