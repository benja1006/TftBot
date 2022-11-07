from window import Window
from Utils.screenCoords import getConsts
import pyautogui
import pytesseract
import os
import time


def trPoint(x: int, y: int, window: Window) -> tuple:
    """Take a point coded for 2560x1440 and returns the transformed value."""
    base_width = 2560
    base_height = 1440

    new_y = y/base_height * window.height + window.y
    new_x = x/base_width * window.width + window.x

    return (new_x, new_y)


def get_round(window: Window):
    consts = getConsts(os.path.join(os.getcwd(), 'screen_coords.txt'))
    top, left = trPoint(consts['ROUND_NUM_TOP'], consts['ROUND_NUM_LEFT'],
                        window)
    bottom, right = trPoint(consts['ROUND_NUM_BOT'], consts['ROUND_NUM_RIGHT'],
                            window)


def update_tk(tk):
    tk.update()
    tk.update_idletasks()


def update_tk_loop(tk, wait_time):
    for i in range(wait_time*10):
        tk.update()
        tk.update_idletasks()
        time.sleep(.1)
