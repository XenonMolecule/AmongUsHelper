import sys
from datetime import datetime
import pyautogui
import cv2
import time
import numpy as np

start = datetime.now()

while True:
    if pyautogui.locateOnScreen('shh_small.png', grayscale=False, confidence=.5):
        break

    # elif (datetime.now() - start).seconds > 30:
        # sys.exit()

    else:
        print('No shh detected')

time.sleep(4.63)
screen = np.array(pyautogui.screenshot())
cv2.imshow("bruh", screen)
cv2.waitKey(0)
