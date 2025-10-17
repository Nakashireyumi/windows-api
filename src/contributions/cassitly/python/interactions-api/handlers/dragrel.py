import pyautogui

async def handle(msg, context):
    dx = msg.get("x")
    dy = msg.get("y")
    if dx is None or dy is None:
        return {"status": "error", "error": {"message": "invalid_params", "details": "Requires 'x' and 'y'"}}
    duration = float(msg.get("duration", 0.0))
    button = msg.get("button", "left")
    pyautogui.dragRel(int(dx), int(dy), duration=duration, button=button)
    return {"status": "ok", "result": {"dragged_rel": [int(dx), int(dy)], "button": button}}