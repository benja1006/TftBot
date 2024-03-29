"""Original champion image capture. Should be depricated."""
import cv2
import os
import screeninfo
import pyautogui
import numpy as np
import time
from pynput import keyboard


monitor_x = screeninfo.get_monitors()[0].width
monitor_y = screeninfo.get_monitors()[0].height

xRatio = monitor_x/2560
yRatio = monitor_y/1440
yTop = int(1237 * yRatio)
yBottom = int(1425 * yRatio)
xStart = int(640 * xRatio)
xWidth = int(257 * xRatio)
xSpacing = int(268 * xRatio)
shopPath = os.path.join(os.getcwd(), "shopChamps")


def screenGrabShop():
    """Grab champ images from screen."""
    indexes = [int(os.path.join(shopPath, f)[len(shopPath)+1:-4])
               for f in os.listdir(shopPath)
               if os.path.isfile(os.path.join(shopPath, f))]
    currIndex = 0
    if indexes != []:
        currIndex = max(indexes) + 1
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    for i in range(0, 5):
        champ = image[yTop:yBottom, xStart + i * xSpacing:xStart + xWidth +
                      i * xSpacing]
        cv2.imwrite(str(os.path.join(shopPath, str(currIndex)))
                    + ".jpg", champ)
        currIndex += 1
    print(currIndex)


# keyboard listening
def on_press(key):
    """Run on key press."""
    if not hasattr(key, 'char'):
        return
    if key.char == 'd':
        print('D Pressed')
        time.sleep(.1)
        screenGrabShop()
    if key.char == 'z':
        print('z Pressed')
        time.sleep(.1)
        screenGrabShop()


def on_release(key):
    """Do nothing."""
    return


with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
