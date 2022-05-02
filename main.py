import numpy as np
import cv2
from mss import mss
from PIL import Image
import sys
import os
import screeninfo


# bounding_box = {'top': 100, 'left': 0, 'width': 400, 'height': 300}
#
# sct = mss()

# while True:
#     sct_img = sct.grab(bounding_box)
#     cv2.imshow('screen', np.array(sct_img))
#
#     if (cv2.waitKey(1) & 0xFF) == ord('q'):
#         cv2.destroyAllWindows()
#         break
def onMouse(event, x, y, flags, param):
    global mouse_x, mouse_y, draw
    if event == cv2.EVENT_LBUTTONDOWN:
        circle = cv2.circle(images[i], (x, y), 20, (0,0,255), 2)
        cv2.imshow("test", circle)
# while True:
#     if (cv2.waitKey(1) & 0xFF) == ord('l'):
#             cv2.destroyAllWindows()
#             break
#
#
#
screen = screeninfo.get_monitors()[0]
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
cv2.moveWindow("test", screen.x - 1, screen.y - 1)
cv2.setWindowProperty("test", 0, 1)
cv2.setMouseCallback('test', onMouse)

imageDirectory = os.path.join(os.getcwd(), "images")
images = [cv2.imread(os.path.join(imageDirectory, f)) for f in os.listdir(imageDirectory) if os.path.isfile(os.path.join(imageDirectory, f))];
i = 0;
while True:

    cv2.imshow("test", images[i])

    cv2.setMouseCallback('test', onMouse)
    k = cv2.waitKey(0)

    if k == ord("s") and i < (len(images)-1):
        i += 1
    if k == ord("a") and i > 0:
        i-= 1
    if k == ord("q"):
        break
