# handlers/move.py
import pyautogui

async def handle(msg, context):
    x = msg.get("x")
    y = msg.get("y")
    duration = float(msg.get("duration", 0.0))
    if x is None or y is None:
        return {"status": "error", "error": {"message": "invalid_params", "details": "Requires 'x' and 'y'"}}
    
    # Get screen size for validation
    screen_width, screen_height = pyautogui.size()
    
    # Validate and clamp coordinates to screen bounds
    x = max(1, min(int(x), screen_width - 2))  # Avoid corners (1 to width-2)
    y = max(1, min(int(y), screen_height - 2))  # Avoid corners (1 to height-2)
    
    pyautogui.moveTo(x, y, duration=duration)
    return {"status": "ok", "result": {"moved_to": [x, y]}}
