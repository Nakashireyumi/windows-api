import pyautogui

async def handle(msg, context):
    x = msg.get("x")
    y = msg.get("y")
    if x is None or y is None:
        return {"status": "error", "error": {"message": "invalid_params", "details": "Requires 'x' and 'y'"}}
    duration = float(msg.get("duration", 0.0))
    button = msg.get("button", "left")
    
    # Get screen size for validation
    screen_width, screen_height = pyautogui.size()
    
    # Validate and clamp coordinates to screen bounds
    x = max(1, min(int(x), screen_width - 2))  # Avoid corners (1 to width-2)
    y = max(1, min(int(y), screen_height - 2))  # Avoid corners (1 to height-2)
    
    pyautogui.dragTo(x, y, duration=duration, button=button)
    return {"status": "ok", "result": {"dragged_to": [x, y], "button": button}}
