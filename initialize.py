from datetime import datetime
import cv2
import os
import pytesseract
import pyautogui
import time
import numpy as np
from fuzzywuzzy import fuzz
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
from color_reader import ColorReader

start = datetime.now()

CREW_ONE = (1163, 1013, 314, 570)
CREW_TWO = (1875, 1018, 311, 541)
CREW_THREE = (2188, 1055, 258, 431)
CREW_FOUR = (918, 1089, 253, 395)
CREW_FIVE = (709, 1090, 215, 315)
CREW_SIX = (2434, 1123, 220, 289)
CREW_SEVEN = (563, 1055, 160, 280)
CREW_EIGHT = (2640, 1049, 159, 288)
CREW_NINE = (2799, 1054, 91, 205)

CREW_POSITIONS = [CREW_ONE, CREW_TWO, CREW_THREE, CREW_FOUR, CREW_FIVE,
                  CREW_SIX, CREW_SEVEN, CREW_EIGHT, CREW_NINE]

# INITIALIZE SETTINGS
# ROOM_TEXT_START_X = 1330
# ROOM_TEXT_START_Y = 1817
# ROOM_TEXT_WIDTH = 685
# ROOM_TEXT_HEIGHT = 140
ROOM_TEXT_START_X = 1030
ROOM_TEXT_START_Y = 1320
ROOM_TEXT_WIDTH = 500
ROOM_TEXT_HEIGHT = 85

SNIP_REGION = (
    ROOM_TEXT_START_X,
    ROOM_TEXT_START_Y,
    ROOM_TEXT_WIDTH,
    ROOM_TEXT_HEIGHT
)

ROOMS = ["Cafeteria", "Weapons", "O2", "Navigation",
         "Shields", "Communications", "Storage", "Admin",
         "Electrical", "Lower Engine", "Security", "Reactor",
         "Upper Engine", "Medbay"]

MIN_STRING_MATCH_RATIO = 60


def segment_crew():
    for f in os.listdir("./player_imgs/"):
        os.remove(os.path.join("./player_imgs/", f))

    screen = np.array(pyautogui.screenshot())
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    screen = cv2.resize(screen, dsize=(3360, 2100), interpolation=cv2.INTER_CUBIC)
    # screen = cv2.imread("segmentation_test.png")

    crew_count, colors = ColorReader.color_reader(screen)
    colors = [color.upper() for color in colors]
    for i in range(crew_count):
        pos = CREW_POSITIONS[i]
        image = screen[pos[1]:pos[1] + pos[3], pos[0]:pos[0] + pos[2]]
        scale_percent = 205.0 / image.shape[0]
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        dim = (width, height)
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        cv2.imwrite("player_imgs/crew" + str(colors[i]) + "-1.png", resized)
        cv2.imwrite("player_imgs/crew" + str(colors[i]) + "-2.png", cv2.flip(resized, 1))

    # cv2.imshow("bruh", screen)
    # cv2.waitKey(0)
    cv2.imwrite("crewmatemenu.png", screen)

# Returns the best guess for the room that the player is in or None if it can't get a good guess
def getPlayerRoom():
    im = pyautogui.screenshot(region=SNIP_REGION)
    im.save('roomname.png')

    background = pyautogui.screenshot()
    background.save('roomname_background.png')

    gray_img = rgb2gray(np.array(im))

    image = gray_img
    try:
        image = gray_img < threshold_otsu(gray_img, 32)
    except:
        pass

    # in order to apply Tesseract v4 to OCR text we must supply
    # (1) a language, (2) an OEM flag of 4, indicating that the we
    # wish to use the LSTM neural net model for OCR, and finally
    # (3) an OEM value, in this case, 7 which implies that we are
    # treating the ROI as a single line of text
    config = ("-l eng --oem 1 --psm 7")
    text = ""
    try:
        text = pytesseract.image_to_string(image, config=config)
        print("text")
    except:
        pass

    best_ratio = MIN_STRING_MATCH_RATIO
    room = None
    for room_name in ROOMS:
        ratio = fuzz.ratio(room_name.lower(), text.lower())
        print("ratio " + str(ratio))
        print(best_ratio)
        if ratio > best_ratio:
            best_ratio = ratio
            room = room_name

    return room

def detect_crewmates(room):
    for img_obj in os.scandir("./player_imgs/"):
        if pyautogui.locateOnScreen("./player_imgs/" + img_obj.name, grayscale=False, confidence=.35):
            name = img_obj.name
            color = name[:-6]
            color = color[4:]
            print("CREW " + color + " - " + room)

while True:
    time.sleep(0.1)
    if pyautogui.locateOnScreen('crewtext.png', grayscale=False, confidence=.5): # shh_small
        break

    # elif (datetime.now() - start).seconds > 30:
        # sys.exit()

    else:
        print('No shh detected')
print("Saw shh")
time.sleep(1) # 2.66

segment_crew()

last_room = "Cafeteria"
while True:
    time.sleep(0.1)
    new_room = getPlayerRoom()
    print(new_room)
    if new_room:
        if last_room != new_room:
            print("Just entered " + new_room)
        last_room = new_room
    detect_crewmates(last_room)
