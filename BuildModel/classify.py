import cv2
import os
import screeninfo
import pytesseract
import re

screen = screeninfo.get_monitors()[0]
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
# cv2.moveWindow("test", screen.x - 1, screen.y - 1)
# cv2.setWindowProperty("test", 0, 1)
draw = False
imageDirectory = os.path.join(os.getcwd(), "shopChamps")
imageNames = [f for f in os.listdir(imageDirectory) if os.path.isfile(os.path.join(imageDirectory, f))]
imageFullPaths = [os.path.join(imageDirectory, f) for f in imageNames]
croppedImages = [cv2.imread(image)[160:182, 10:105] for image in imageFullPaths]

for i, img in enumerate(croppedImages):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)


    im2 = img.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]


        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        text = text[0:-1]
        text = re.sub(r'\W+', '', text)
        # Move the uncropped file
        if text == "":
            os.rename(imageFullPaths[i], os.path.join(os.getcwd(), "champs", "unknown", imageNames[i]))
            continue
        newFolder = os.path.join(os.getcwd(), "champs", text)
        if not os.path.isdir(newFolder):
            os.mkdir(newFolder)
        os.rename(imageFullPaths[i], os.path.join(newFolder, imageNames[i]))

        # Close the file
