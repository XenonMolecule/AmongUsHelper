import sys
from datetime import datetime
import pyautogui

start = datetime.now()

while True: 
    if pyautogui.locateOnScreen('shh.png', grayscale=False, confidence=.5):
        break

    elif (datetime.now() - start).seconds > 30:
        sys.exit()

    else:
        print('No shh detected')

