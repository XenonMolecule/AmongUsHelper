import pyautogui
import time

time.sleep(2)
print(pyautogui.locateOnScreen('Xenon.png', confidence=.5))