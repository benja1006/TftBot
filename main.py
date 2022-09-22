import cv2
import os
import screeninfo
import pyautogui
import numpy as np
import time
from pyinput import keyboard


yTop = 1237
yBottom = 1425
xStart = 640
xWidth = 257
xSpacing = 268
shopPath = os.path.join(os.getcwd(), "shopChamps")


# keyboard listening
def on_press(key):
    if key == keyboard.Key.d:
        time.sleep(.1)
        screenGrabShop()


def on_release(key):
    if key == keyboard.Key.q:
        return False


with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()


def screenGrabShop():
    indexes = [os.path.join(shopPath, f)[0:-4] for f in os.listdir(shopPath) if os.path.isFile(os.path.join(shopPath, f))]
    currIndex = 0
    if indexes != []:
        currIndex = max(indexes)
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    for i in range(0, 5):
        champ = image[yTop:yBottom, xStart + i * xSpacing:xStart + xWidth + i * xSpacing]
        cv2.imwrite(str(os.path.join(shopPath, str(currIndex))) + ".jpg", champ)
        currIndex += 1


cv2.namedWindow("test", cv2.WINDOW_NORMAL)

while True:

    k = cv2.waitKey(0)

    if k == ord("d"):
        time.sleep(.1)
        screenGrabShop()
    if k == ord("q"):
        break
