
import cv2
import os
import screeninfo


def onMouse(event, x, y, flags, param):
    global start_x, start_y, draw
    if event == cv2.EVENT_LBUTTONDOWN:

        if not draw:
            start_x, start_y = x, y
            print(str(x) + " " + str(y))
            draw = True
            return
    elif event == cv2.EVENT_LBUTTONUP:
        draw = False
        line = cv2.rectangle(images[i], (start_x, start_y), (x, y), (0, 0, 255), 2)
        cv2.imshow("test", line)
        print(str(x) + " " + str(y))


screen = screeninfo.get_monitors()[0]
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
cv2.moveWindow("test", screen.x - 1, screen.y - 1)
cv2.setWindowProperty("test", 0, 1)
cv2.setMouseCallback('test', onMouse)
draw = False
imageDirectory = os.path.join(os.getcwd(), "images")
images = [cv2.imread(os.path.join(imageDirectory, f)) for f in os.listdir(imageDirectory) if os.path.isfile(os.path.join(imageDirectory, f))];
i = 0
while True:

    cv2.imshow("test", images[i])

    cv2.setMouseCallback('test', onMouse)
    k = cv2.waitKey(0)

    if k == ord("s") and i < (len(images)-1):
        i += 1
    if k == ord("a") and i > 0:
        i -= 1
    if k == ord("q"):
        break
