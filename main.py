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

yTop = 1237
yBottom = 1425
xStart = 640
xWidth = 257
xSpacing = 268
for i, image in enumerate(images):
    for x in range(0, 5):
        rect = cv2.rectangle(image, (xStart + x * xSpacing, yTop), (xStart + xWidth + x * xSpacing, yBottom), (0, 0, 255), 2)
        cv2.imshow('image', rect)

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
