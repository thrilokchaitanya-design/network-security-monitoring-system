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