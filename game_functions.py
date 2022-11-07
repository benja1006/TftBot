from window import Window
from Utils.game_utils import *
import pyautogui
import pytesseract
import os
import time
import cv2


def trPoint(x: int, y: int, window: Window) -> tuple:
    """Take a point coded for 2560x1440 and returns the transformed value."""
    base_width = 2560
    base_height = 1440

    new_y = y/base_height * window.height + window.y
    new_x = x/base_width * window.width + window.x

    return (new_x, new_y)


def get_round(window: Window) -> str:
    consts = getConsts(os.path.join(os.getcwd(), 'screen_coords.txt'))
    top, left = trPoint(consts['ROUND_NUM_TOP'], consts['ROUND_NUM_LEFT'],
                        window)
    bottom, right = trPoint(consts['ROUND_NUM_BOT'], consts['ROUND_NUM_RIGHT'],
                            window)
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cropped_image = image[top:bottom, left:right]
    roundstr = get_text_from_image(image)
    print('Current round: ' + roundstr)
    return roundstr


def update_tk(tk):
    tk.update()
    tk.update_idletasks()


def update_tk_loop(tk, wait_time):
    for i in range(wait_time*10):
        tk.update()
        tk.update_idletasks()
        time.sleep(.1)
