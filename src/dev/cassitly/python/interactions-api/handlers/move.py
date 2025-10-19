# handlers/move.py
import pyautogui

async def handle(msg, context):
    x = msg.get("x")
    y = msg.get("y")
    duration = float(msg.get("duration", 0.0))
    if x is None or y is None:
        return {"status": "error", "error": {"message": "invalid_params", "details": "Requires 'x' and 'y'"}}
    pyautogui.moveTo(int(x), int(y), duration=duration)
    return {"status": "ok", "result": {"moved_to": [int(x), int(y)]}}