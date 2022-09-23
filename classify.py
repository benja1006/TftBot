import cv2
import os
import screeninfo

screen = screeninfo.get_monitors()[0]
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
cv2.moveWindow("test", screen.x - 1, screen.y - 1)
cv2.setWindowProperty("test", 0, 1)
draw = False
imageDirectory = os.path.join(os.getcwd(), "shopChamps")
images = [cv2.imread(os.path.join(imageDirectory, f)) for f in os.listdir(imageDirectory) if os.path.isfile(os.path.join(imageDirectory, f))];
i = 0

while True:

    cv2.imshow("test", images[i])

    k = cv2.waitKey(0)

    if k == ord("s") and i < (len(images)-1):
        i += 1
    if k == ord("a") and i > 0:
        i -= 1
    if k == ord("q"):
        break
