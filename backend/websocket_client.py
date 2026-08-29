import asyncio
import websockets


async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/alerts"

    print(f"Connecting to {uri}...")

    async with websockets.connect(uri) as websocket:
        print("WebSocket connected successfully!")
        print("Waiting for real-time alerts...\n")

        while True:
            message = await websocket.recv()
            print("REAL-TIME ALERT RECEIVED:")
            print(message)
            print()


asyncio.run(test_websocket())