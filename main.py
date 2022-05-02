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
# def onMouse(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         if (cv2.waitKey(1) & 0xFF) == ord('q'):
#             print("'top': " + y)
#         if (cv2.waitKey(1) & 0xFF) == ord('e'):
#             print("bottom: " + y)
#         if (cv2.waitKey(1) & 0xFF) == ord('w'):
#             print("right: " + x)
#         if (cv2.waitKey(1) & 0xFF) == ord('r'):
#             print("'left': " + x)
# while True:
#     if (cv2.waitKey(1) & 0xFF) == ord('l'):
#             cv2.destroyAllWindows()
#             break
#
#
#
#     cv2.setMouseCallback('WindowName', onMouse)
screen = screeninfo.get_monitors()[0]
imageDirectory = os.path.join(os.getcwd(), "images")
images = [cv2.imread(os.path.join(imageDirectory, f)) for f in os.listdir(imageDirectory) if os.path.isfile(os.path.join(imageDirectory, f))];
i = 0;
while True:
    cv2.namedWindow("test", cv2.WINDOW_NORMAL)
    cv2.moveWindow("test", screen.x - 1, screen.y - 1)
    cv2.setWindowProperty("test", 0, 1)
    cv2.imshow("test", images[i])
    k = cv2.waitKey(0)

    if k == ord("s"):
        i += 1
        if i == len(images):
            break
    if k == ord("q"):
        break
