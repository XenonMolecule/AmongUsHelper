import pyautogui
import cv2
import os
import time
import numpy as np

CREW_ONE = (1163, 1013, 314, 570)
CREW_TWO = (1875, 1018, 311, 541)
CREW_THREE = (918, 1089, 253, 395)
CREW_FOUR = (2188, 1055, 258, 431)
CREW_FIVE = (709, 1090, 215, 315)
CREW_SIX = (2434, 1123, 220, 289)
CREW_SEVEN = (563, 1055, 160, 280)
CREW_EIGHT = (2640, 1049, 159, 288)
CREW_NINE = (2799, 1054, 91, 205)

CREW_POSITIONS = [CREW_ONE, CREW_TWO, CREW_THREE, CREW_FOUR, CREW_FIVE,
                  CREW_SIX, CREW_SEVEN, CREW_EIGHT, CREW_NINE]


def segment_crew(crew_count):
    for f in os.listdir("./player_imgs/"):
        os.remove(os.path.join("./player_imgs/", f))

    screen = np.array(pyautogui.screenshot())
    cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    screen = cv2.resize(screen, dsize=(3360, 2100), interpolation=cv2.INTER_CUBIC)
    # screen = cv2.imread("segmentation_test.png")

    for i in range(crew_count):
        pos = CREW_POSITIONS[i]
        image = screen[pos[1]:pos[1] + pos[3], pos[0]:pos[0] + pos[2]]
        cv2.imwrite("player_imgs/crew" + str(i + 1) + "-1.png", image)
        cv2.imwrite("player_imgs/crew" + str(i + 1) + "-2.png", cv2.flip(image, 1))


time.sleep(4)
segment_crew(9)
