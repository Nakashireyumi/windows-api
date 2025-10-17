# src/contributions/cassitly/python/examples/gui-client/__main__.py
# This file path is for vibe coders lol

import asyncio
import json
import websockets
import yaml
from pathlib import Path

# Load configuration
CONFIG_PATH = Path(__file__).resolve().parents[5] / "resources" / "gui" / "config" / "authentication.yaml"

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing configuration file: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

async def test():
    config = load_config()
    host = config.get("host", "127.0.0.1")
    port = config.get("port", 8765)
    token = config.get("auth_token")
    uri = f"ws://{host}:{port}"

    async with websockets.connect(uri) as ws:
        # Move mouse
        await ws.send(json.dumps({"token": token, "action": "move", "x": 500, "y": 400, "duration": 0.2}))
        print(await ws.recv())

        # Click
        await ws.send(json.dumps({"token": token, "action": "click", "button": "left"}))
        print(await ws.recv())

        # Type text
        await ws.send(json.dumps({"token": token, "action": "type", "text": "Hello from WebSocket!", "interval": 0.02}))
        print(await ws.recv())

        # Screenshot full screen
        await ws.send(json.dumps({"token": token, "action": "screenshot"}))
        print(await ws.recv())

asyncio.run(test())