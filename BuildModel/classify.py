"""Classify and sort the unsorted champion images using ocr."""
import cv2
import os
import screeninfo
import pytesseract
import re
import random
import time
import math

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Jorda\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

screen = screeninfo.get_monitors()[0]
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
# cv2.moveWindow("test", screen.x - 1, screen.y - 1)
# cv2.setWindowProperty("test", 0, 1)
draw = False
imageDirectory = os.path.join(os.getcwd(), "UnsortedChampImages")
imageNames = [f for f in os.listdir(imageDirectory)
              if os.path.isfile(os.path.join(imageDirectory, f))]
imageFullPaths = [os.path.join(imageDirectory, f) for f in imageNames]
croppedImages = [cv2.imread(image)[160:182, 10:105]
                 for image in imageFullPaths]

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
        if not os.path.exists(imageFullPaths[i]):
            break
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        text = text[0:-1]
        text = re.sub(r'\W+', '', text)
        new_f_name = str(math.floor((time.time()*1000))) + ".jpg"
        # Move the uncropped file
        if text == "":
            assert os.path.exists(imageFullPaths[i])
            # assert os.path.exists(os.path.join(os.getcwd(),
            #           "BuildModel", "unknownChamps", new_f_name))
            os.rename(imageFullPaths[i], os.path.join(os.getcwd(),
                      "BuildModel", "unknownChamps", new_f_name))
            continue
        
        newFolder = os.path.join(os.getcwd(), "BuildModel", "champs", text)
        if not os.path.isdir(newFolder):
            os.mkdir(newFolder)
        os.rename(imageFullPaths[i], os.path.join(newFolder, new_f_name))

        # Close the file
