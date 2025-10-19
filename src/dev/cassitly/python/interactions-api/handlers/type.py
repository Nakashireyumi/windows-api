import pyautogui
import time

async def handle(msg, context):
    text = msg.get("text", "")
    interval = float(msg.get("interval", 0.02))
    
    if not isinstance(text, str) or not text:
        return {"status": "error", "error": {"message": "No text to type"}}
    
    pyautogui.typewrite(text, interval=interval)
    time.sleep(0.05)
    return {"status": "ok", "result": {"typed": text}}
