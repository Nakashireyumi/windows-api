import datetime, pyautogui

async def handle(msg, context):
    screenshot_dir = context["screenshot_dir"]
    name = msg.get("name")
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = name if (isinstance(name, str) and name.strip()) else f"snap_{ts}.png"
    path = screenshot_dir / filename
    region = msg.get("region")
    if isinstance(region, list) and len(region) == 4:
        x, y, w, h = map(int, region)
        img = pyautogui.screenshot(region=(x, y, w, h))
    else:
        img = pyautogui.screenshot()
    img.save(path)
    return {"status": "ok", "result": {"saved": str(path.resolve())}}