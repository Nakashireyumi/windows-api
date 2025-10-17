import asyncio
import json
import websockets

AUTH_TOKEN = "replace-with-a-strong-secret"

async def test():
    async with websockets.connect("ws://127.0.0.1:8765") as ws:
        # Move mouse
        await ws.send(json.dumps({"token": AUTH_TOKEN, "action": "move", "x": 500, "y": 400, "duration": 0.2}))
        print(await ws.recv())

        # Click
        await ws.send(json.dumps({"token": AUTH_TOKEN, "action": "click", "button": "left"}))
        print(await ws.recv())

        # Type text
        await ws.send(json.dumps({"token": AUTH_TOKEN, "action": "type", "text": "Hello from WebSocket!", "interval": 0.02}))
        print(await ws.recv())

        # Screenshot full screen
        await ws.send(json.dumps({"token": AUTH_TOKEN, "action": "screenshot"}))
        print(await ws.recv())

asyncio.run(test())