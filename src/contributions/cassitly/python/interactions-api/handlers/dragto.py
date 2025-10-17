import pyautogui

async def handle(msg, context):
    x = msg.get("x")
    y = msg.get("y")
    if x is None or y is None:
        return {"status": "error", "error": {"message": "invalid_params", "details": "Requires 'x' and 'y'"}}
    duration = float(msg.get("duration", 0.0))
    button = msg.get("button", "left")
    pyautogui.dragTo(int(x), int(y), duration=duration, button=button)
    return {"status": "ok", "result": {"dragged_to": [int(x), int(y)], "button": button}}