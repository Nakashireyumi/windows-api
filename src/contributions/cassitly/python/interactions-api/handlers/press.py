import pyautogui

async def handle(msg, context):
    key = msg.get("key")
    if not key:
        return {"status": "error", "error": {"message": "invalid_params", "details": "Requires 'key'"}}
    pyautogui.press(str(key))
    return {"status": "ok", "result": {"pressed": key}}