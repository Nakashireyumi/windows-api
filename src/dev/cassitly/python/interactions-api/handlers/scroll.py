import pyautogui

async def handle(msg, context):
    clicks = int(msg.get("clicks", 0))
    x = msg.get("x")
    y = msg.get("y")
    if x is not None and y is not None:
        pyautogui.moveTo(int(x), int(y))
    pyautogui.scroll(clicks)
    return {"status": "ok", "result": {"scrolled": clicks}}