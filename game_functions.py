"""Functions needed for the game to work."""
from window import Window
from Utils.game_utils import get_text_from_image, save_image
import pyautogui
import os
import time
import cv2
import Utils.grabChampImages as gci
import numpy as np
import screen_coords as sc
import re


def trPoint(x: int, y: int, window: Window) -> tuple:
    """Take a point coded for 2560x1440 and returns the transformed value."""
    base_width = 2560
    base_height = 1440

    new_y = y/base_height * window.height + window.y
    new_x = x/base_width * window.width + window.x

    return (int(new_x), int(new_y))


def trX(x: int, window: Window) -> int:
    """Transform an X coordinate to the current window."""
    base_width = 2560
    new_x = x/base_width * window.width + window.x

    return int(new_x)


def trY(y: int, window: Window) -> int:
    """Transform a Y coordinate to the current window."""
    base_height = 1440
    new_y = y/base_height * window.height + window.y
    return int(new_y)


def get_round(window: Window) -> str:
    """Return the current round."""
    # def top bot left right
    top = trY(sc.ROUND_NUM_TOP, window)
    bottom = trY(sc.ROUND_NUM_BOT, window)
    left = trX(sc.ROUND_NUM_LEFT, window)
    right = trX(sc.ROUND_NUM_RIGHT, window)

    # grab the screen shot
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cropped_image = image[top:bottom, left:right]
    roundstr = get_text_from_image(cropped_image)
    if re.match(r"(\s*[0-9]-[0-9]\s*)", roundstr):
        print('Current round: ' + roundstr)
        return roundstr
    left = trX(sc.ROUND_NUM_START_LEFT, window)
    right = trX(sc.ROUND_NUM_START_RIGHT, window)
    cropped_image = image[top:bottom, left:right]
    roundstr = get_text_from_image(cropped_image)
    if re.match(r"(\s*[0-9]-[0-9]\s*)", roundstr):
        print('Current round: ' + roundstr)
        return roundstr

    return ""


def update_tk(tk):
    """Update the tk window once."""
    tk.update()
    tk.update_idletasks()


def update_tk_loop(tk, wait_time, dPressed):
    """Continuously update the tk window for duration of wait_time."""
    for i in range(wait_time*10):
        # break this loop if the d key is pressed
        tk.update()
        tk.update_idletasks()
        if dPressed:
            break
        time.sleep(.1)


def get_curr_champs(window: Window, interpreter, labels) -> [()]:
    """Return the current champs along with which slot they are in."""
    # yTop, yBottom, xLeft, xRight, xSpacing
    yTop = trY(sc.CHAMP_TOP, window)
    yBottom = trY(sc.CHAMP_BOT, window)
    xLeft = trX(sc.CHAMP_LEFT, window)
    xRight = trX(sc.CHAMP_RIGHT, window)
    xSpacing = trX(sc.CHAMP_SPACING, window)

    images = gci.screenGrabShop(yTop, yBottom, xLeft, xRight, xSpacing)
    # now classify the images using tf model

    curr_champs = []
    for idx, img in enumerate(images):
        curr_champs.append((gci.predictImage(img, interpreter, labels), idx))
        champ_path = os.path.join(os.getcwd(), 'UnsortedChampImages')
        save_image(champ_path, img)
    return curr_champs
