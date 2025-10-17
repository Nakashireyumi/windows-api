import asyncio, json, traceback, importlib, pkgutil
from pathlib import Path
import yaml

import pyautogui
import websockets

# ---------------------------
# Load configuration from YAML
# ---------------------------
def load_config():
    # Find base directory relative to this file
    base_dir = Path(__file__).resolve().parent  # directory where THIS script lives
    config_path = base_dir / "src/resources/gui/config/authentication.yaml"

    # Optional: if file not found, fallback to project root
    if not config_path.exists():
        # Search upwards (useful if launched from another directory)
        project_root = Path(__file__).resolve().parents[2]  # adjust as needed
        config_path = project_root / "src/resources/gui/config/authentication.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

cfg = load_config()

HOST = cfg.get("host", "127.0.0.1")
PORT = int(cfg.get("port", 8765))
AUTH_TOKEN = cfg.get("auth_token", "replace-with-a-strong-secret")
SCREENSHOT_DIR = Path(cfg.get("screenshot_dir", "./screenshots"))

# Basic safety defaults
pyautogui.FAILSAFE = bool(cfg.get("failsafe", True))
pyautogui.PAUSE = float(cfg.get("pause", 0.05))

# Ensure screenshot directory exists
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# Load all handlers dynamically
# ---------------------------

handlers = {}

def load_handlers():
    from . import handlers as package
    for _, modname, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{__package__}.handlers.{modname}")
        if hasattr(module, "handle"):
            handlers[modname] = module.handle

load_handlers()

# ---------------------------
# Utilities
# ---------------------------

def ok(payload=None):
    return json.dumps({"status": "ok", "result": payload or {}})

def err(message, details=None):
    return json.dumps({"status": "error", "error": {"message": message, "details": details or ""}})

# ---------------------------
# Dispatcher
# ---------------------------

async def handle_message(msg: dict) -> str:
    if msg.get("token") != AUTH_TOKEN:
        return err("unauthorized")

    action = msg.get("action")
    if not action or not isinstance(action, str):
        return err("invalid_action", "Missing or non-string 'action'")

    # --- Dynamic reload hook ---
    if action == "reload":
        try:
            handlers.clear()
            load_handlers()
            return ok({"message": "Handlers reloaded", "count": len(handlers)})
        except Exception as e:
            return err("reload_failed", {"exception": str(e), "traceback": traceback.format_exc()})

    handler = handlers.get(action)
    if not handler:
        return err("unsupported_action", f"Action '{action}' not supported")

    try:
        result = await handler(msg, {"screenshot_dir": SCREENSHOT_DIR})
        return json.dumps(result)
    except Exception as e:
        return err("executionerror", {"exception": str(e), "traceback": traceback.format_exc()})

# ---------------------------
# WebSocket Server
# ---------------------------

async def handler(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            await websocket.send(err("invalid_json"))
            continue
        response = await handle_message(data)
        await websocket.send(response)

async def main():
    async with websockets.serve(handler, HOST, PORT, max_size=2**20):  # 1 MiB limit
        print(f"WebSocket GUI server listening on ws://{HOST}:{PORT}")
        print("Press Ctrl+C to stop.")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")