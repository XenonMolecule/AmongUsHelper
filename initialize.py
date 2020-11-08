from utilities import *

import sys
from datetime import datetime
import time
import numpy as np
import cv2
import pyautogui

def main():
    start = datetime.now()

    while True: 
        if pyautogui.locateOnScreen('assets/shh.png', grayscale=False, confidence=.5):
            break
        elif (datetime.now() - start).seconds > 30:
            sys.exit()
            print('Timeout')
        else:
            print('No shh detected')

    time.sleep(4.2)
    cv2.imwrite('assets/tmp/crewmate_screenshot.png', cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR))
    color_reader('assets/tmp/crewmate_screenshot.png')
    
    ## segement_crew & roomtracker

if __name__ == '__main__':
    main()