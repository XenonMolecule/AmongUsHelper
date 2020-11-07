# import the necessary packages
import pytesseract
import pyautogui
import time
import numpy as np
from fuzzywuzzy import fuzz
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray


# INITIALIZE SETTINGS
ROOM_TEXT_START_X = 1330
ROOM_TEXT_START_Y = 1817
ROOM_TEXT_WIDTH = 685
ROOM_TEXT_HEIGHT = 140

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

# Returns the best guess for the room that the player is in or None if it can't get a good guess
def getPlayerRoom():
    im = pyautogui.screenshot(region=SNIP_REGION)

    gray_img = rgb2gray(np.array(im))

    image = gray_img < threshold_otsu(gray_img, 32)
    # in order to apply Tesseract v4 to OCR text we must supply
    # (1) a language, (2) an OEM flag of 4, indicating that the we
    # wish to use the LSTM neural net model for OCR, and finally
    # (3) an OEM value, in this case, 7 which implies that we are
    # treating the ROI as a single line of text
    config = ("-l eng --oem 1 --psm 7")
    text = pytesseract.image_to_string(image, config=config)

    best_ratio = MIN_STRING_MATCH_RATIO
    room = None
    for room_name in ROOMS:
        ratio = fuzz.ratio(room_name.lower(), text.lower())
        if ratio > best_ratio:
            best_ratio = ratio
            room = room_name

    return room


while True:
    time.sleep(1)
    print(getPlayerRoom())
