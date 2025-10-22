import pyautogui

async def handle(msg, context):
    x = msg.get("x")
    y = msg.get("y")
    button = msg.get("button", "left")
    
    # Get screen size for validation
    screen_width, screen_height = pyautogui.size()

    # Move first if coordinates provided
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        # Validate and clamp coordinates to screen bounds
        x = max(1, min(int(x), screen_width - 2))  # Avoid corners (1 to width-2)
        y = max(1, min(int(y), screen_height - 2))  # Avoid corners (1 to height-2)
        pyautogui.moveTo(x, y)
    
    pyautogui.click(button=button)
    return {"status": "ok", "result": {"clicked": [x, y], "button": button}}
