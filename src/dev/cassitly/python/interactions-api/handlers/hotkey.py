# src/gui/handlers/hotkey.py
import pyautogui
import asyncio
import json

async def handle(msg: dict, ctx: dict):
    """
    Example hotkey handler.
    Expected JSON:
    {
        "token": "...",
        "action": "hotkey",
        "keys": ["ctrl", "alt", "del"]
    }
    """
    keys = msg.get("keys")
    if not keys or not isinstance(keys, list):
        return {"status": "error", "error": {"message": "Missing or invalid 'keys' list"}}

    try:
        # Run hotkey in thread-safe way (pyautogui is blocking)
        await asyncio.to_thread(pyautogui.hotkey, *keys)
        return {"status": "ok", "result": {"message": f"Pressed hotkey: {'+'.join(keys)}"}}
    except Exception as e:
        return {
            "status": "error",
            "error": {
                "message": "Failed to execute hotkey",
                "details": str(e)
            }
        }
