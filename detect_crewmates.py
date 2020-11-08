import pyautogui
import time
import os


def detect_crewmates():
    for img_obj in os.scandir("./player_imgs/"):
        if pyautogui.locateOnScreen("./player_imgs/" + img_obj.name, grayscale=False, confidence=.5):
            print(img_obj.name[4])

while True:
    time.sleep(1)
    detect_crewmates()
