from window import Window
from Utils.game_utils import get_coords, get_text_from_image, save_image
import pyautogui
import os
import time
import cv2
import Utils.getChampImages as gci
import numpy as np
import tensorflow as tf


def trPoint(x: int, y: int, window: Window) -> tuple:
    """Take a point coded for 2560x1440 and returns the transformed value."""
    base_width = 2560
    base_height = 1440

    new_y = y/base_height * window.height + window.y
    new_x = x/base_width * window.width + window.x

    return (new_x, new_y)


def trX(x: int, window: Window) -> int:
    base_width = 2560
    new_x = x/base_width * window.width + window.x

    return new_x


def trY(y: int, window: Window) -> int:
    base_height = 1440
    new_y = y/base_height * window.height + window.y
    return new_y


def get_round(window: Window) -> str:
    consts = get_coords(os.path.join(os.getcwd(), 'screen_coords.txt'))
    top, left = trPoint(consts['ROUND_NUM_TOP'], consts['ROUND_NUM_LEFT'],
                        window)
    bottom, right = trPoint(consts['ROUND_NUM_BOT'], consts['ROUND_NUM_RIGHT'],
                            window)
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cropped_image = image[top:bottom, left:right]
    roundstr = get_text_from_image(cropped_image)
    print('Current round: ' + roundstr)
    return roundstr


def update_tk(tk):
    tk.update()
    tk.update_idletasks()


def update_tk_loop(tk, wait_time):
    for i in range(wait_time*10):
        # break this loop if the d key is pressed
        tk.update()
        tk.update_idletasks()
        time.sleep(.1)


def get_curr_champs(window: Window) -> [()]:
    # yTop, yBottom, xLeft, xRight, xSpacing
    coords = get_coords(os.path.join(os.getcwd(), 'screen_coords.txt'))
    yTop = trY(coords['CHAMP_TOP'], window)
    yBottom = trY(coords['CHAMP_BOT'], window)
    xLeft = trX(coords['CHAMP_LEFT'], window)
    xRight = trX(coords['CHAMP_RIGHT'], window)
    xSpacing = trX(coords['CHAMP_SPACING'], window)

    images = gci.screenGrabShop(yTop, yBottom, xLeft, xRight, xSpacing)
    # now classify the images using tf model
    TF_MODEL_FILE_PATH = 'model.tflite'
    labels = gci.getLabels(os.path.join(os.getcwd(), 'labels.txt'))
    interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
    curr_champs = []
    for idx, img in enumerate(images):
        curr_champs.append((gci.predictImage(img, interpreter, labels), idx))
        champ_path = os.join(os.getcwd(), 'UnsortedChampImages')
        save_image(champ_path, img)
    return curr_champs
