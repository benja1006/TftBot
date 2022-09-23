import cv2
import os
import screeninfo
import pytesseract

screen = screeninfo.get_monitors()[0]
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
# cv2.moveWindow("test", screen.x - 1, screen.y - 1)
# cv2.setWindowProperty("test", 0, 1)
draw = False
imageDirectory = os.path.join(os.getcwd(), "shopChamps")
images = [cv2.imread(os.path.join(imageDirectory, f)) for f in os.listdir(imageDirectory) if os.path.isfile(os.path.join(imageDirectory, f))]
croppedImages = [image[160:182, 10:105] for image in images]
i = 0

while True:
    img = cv2.imread(croppedImages[i])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    # open and clear file
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()
    im2 = img.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Open the file in append mode
        file = open("recognized.txt", "a")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        # Appending the text into file
        file.write(text)
        file.write("\n")

        # Close the file
        file.close
    cv2.imshow("test", im2)

    k = cv2.waitKey(0)

    if k == ord("s") and i < (len(croppedImages)-1):
        i += 1
    if k == ord("a") and i > 0:
        i -= 1
    if k == ord("q"):
        break
