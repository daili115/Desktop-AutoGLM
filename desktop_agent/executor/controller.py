import time
import numpy as np
from PIL import Image

try:
    import pyautogui
    import mss
    HAS_GUI = True
except ImportError:
    HAS_GUI = False

class DesktopController:
    def __init__(self):
        if HAS_GUI:
            pyautogui.FAILSAFE = True
            self.screen_width, self.screen_height = pyautogui.size()
        else:
            self.screen_width, self.screen_height = 1920, 1080
            print("Warning: GUI libraries not found. Running in simulation mode.")

    def get_screenshot(self, path: str = "screenshot.png"):
        if not HAS_GUI:
            # Create a dummy screenshot for simulation
            img = Image.new('RGB', (self.screen_width, self.screen_height), color = (73, 109, 137))
            img.save(path)
            return path
            
        with mss.mss() as sct:
            # Get raw pixels from the screen
            sct_img = sct.grab(sct.monitors[1])
            # Convert to PIL Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(path)
        return path

    def tap(self, x: int, y: int):
        if HAS_GUI:
            pyautogui.click(x, y)
        else:
            print(f"Simulating Tap at ({x}, {y})")
        time.sleep(0.5)

    def double_tap(self, x: int, y: int):
        if HAS_GUI:
            pyautogui.doubleClick(x, y)
        else:
            print(f"Simulating DoubleTap at ({x}, {y})")
        time.sleep(0.5)

    def type_text(self, text: str):
        if HAS_GUI:
            pyautogui.write(text, interval=0.1)
        else:
            print(f"Simulating Type: {text}")
        time.sleep(0.5)

    def press_key(self, key: str):
        if HAS_GUI:
            pyautogui.press(key)
        else:
            print(f"Simulating Press: {key}")
        time.sleep(0.5)

    def scroll(self, clicks: int):
        if HAS_GUI:
            pyautogui.scroll(clicks)
        else:
            print(f"Simulating Scroll: {clicks} clicks")
        time.sleep(0.5)

    def drag(self, x1: int, y1: int, x2: int, y2: int, duration: float = 1.0):
        if HAS_GUI:
            pyautogui.moveTo(x1, y1)
            pyautogui.dragTo(x2, y2, duration=duration)
        else:
            print(f"Simulating Drag from ({x1}, {y1}) to ({x2}, {y2})")
        time.sleep(0.5)

    def wait(self, seconds: float):
        time.sleep(seconds)
