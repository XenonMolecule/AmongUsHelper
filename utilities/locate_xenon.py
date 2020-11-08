import pyautogui
import time

time.sleep(2)
print(pyautogui.locateOnScreen('Xenon.png', grayscale=False, confidence=.5))