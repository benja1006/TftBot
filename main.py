import cv2
import os
import screeninfo


def onMouse(event, x, y, flags, param):
    return


screen = screeninfo.get_monitors()[0]
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.moveWindow("image", screen.x - 1, screen.y - 1)
cv2.setWindowProperty("image", 0, 1)
cv2.setMouseCallback('image', onMouse)
draw = False
imageDirectory = os.path.join(os.getcwd(), "images")
images = [cv2.imread(os.path.join(imageDirectory, f)) for f in os.listdir(imageDirectory) if os.path.isfile(os.path.join(imageDirectory, f))];
i = 0
while True:

    cv2.imshow("image", images[i])

    cv2.setMouseCallback('image', onMouse)
    k = cv2.waitKey(0)

    if k == ord("s") and i < (len(images)-1):
        i += 1
    if k == ord("a") and i > 0:
        i -= 1
    if k == ord("q"):
        break
