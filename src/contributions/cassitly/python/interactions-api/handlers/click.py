import pyautogui

async def handle(msg, context):
    x = msg.get("x")
    y = msg.get("y")
    button = msg.get("button", "left")

    # Move first if coordinates provided
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        pyautogui.moveTo(x, y)
    
    pyautogui.click(button=button)
    return {"status": "ok", "result": {"clicked": [x, y], "button": button}}
