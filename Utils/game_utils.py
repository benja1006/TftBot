"""Some utilities needed for the game and game funcitons to run."""
import cv2
import pytesseract
import random
import os


def get_text_from_image(img):
    """Return the text in the image."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    im2 = img.copy()
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)

    # Drawing a rectangle on copied image
    # rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]

    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped)
    text = text[0:-1]
    return pytesseract.image_to_string(cropped,
                                       config='--psm 7 -c '
                                       'tessedit_char_whitelist=""').strip()


def save_image(path, img):
    """Save an image to the desired path  with a random name."""
    name = str(random.randint(1, 100000000)) + '.jpg'
    path = os.path.join(path, name)
    cv2.imwrite(path, img)
