import pyautogui
import time
import mss
import numpy as np
from PIL import Image

class DesktopController:
    def __init__(self):
        pyautogui.FAILSAFE = True
        self.screen_width, self.screen_height = pyautogui.size()

    def get_screenshot(self, path: str = "screenshot.png"):
        with mss.mss() as sct:
            # Get raw pixels from the screen
            sct_img = sct.grab(sct.monitors[1])
            # Convert to PIL Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(path)
        return path

    def tap(self, x: int, y: int):
        pyautogui.click(x, y)
        time.sleep(0.5)

    def double_tap(self, x: int, y: int):
        pyautogui.doubleClick(x, y)
        time.sleep(0.5)

    def type_text(self, text: str):
        pyautogui.write(text, interval=0.1)
        time.sleep(0.5)

    def press_key(self, key: str):
        pyautogui.press(key)
        time.sleep(0.5)

    def scroll(self, clicks: int):
        pyautogui.scroll(clicks)
        time.sleep(0.5)

    def drag(self, x1: int, y1: int, x2: int, y2: int, duration: float = 1.0):
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2, duration=duration)
        time.sleep(0.5)

    def wait(self, seconds: float):
        time.sleep(seconds)
