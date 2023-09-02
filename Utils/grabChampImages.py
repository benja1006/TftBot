"""Utilities surrounding the screen capture of champions."""
import tensorflow as tf
import cv2
import numpy as np
import pyautogui


def screenGrabShop(yTop, yBottom, xLeft, xRight, xSpacing):
    """Get the images of champs in the shop."""
    xWidth = xRight-xLeft

    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    images = []
    for i in range(0, 5):
        champ = image[yTop:yBottom, xLeft + i * xSpacing:xLeft + xWidth +
                      i * xSpacing]
        images.append(champ)
    return images


def predictImage(image, interpreter, class_names):
    """Predict the champ in a given image."""
    # # get image
    img_array = tf.keras.utils.img_to_array(image)
    img_array = tf.image.resize(img_array, [25, 35])
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # build classifier
    classify_lite = interpreter.get_signature_runner('serving_default')
    classify_lite
    predictions_lite = classify_lite(rescaling_1_input=img_array)['dense_1']
    score_lite = tf.nn.softmax(predictions_lite)

    print(
        "This image most likely belongs to {} with a {:.2f} percent "
        "confidence."
        .format(class_names[np.argmax(score_lite)], 100 * np.max(score_lite))
    )
    result = class_names[np.argmax(score_lite)]
    return result


def getLabels(labelFile):
    """Return all labels in order from labels file."""
    f = open(labelFile, 'r')
    cost = 0
    labels = []
    for line in f:
        if line == '' or line=='\n':
            continue
        if line[0].isnumeric():
            cost = line[0]
            continue
        name = line.split('(')[0]
        labels.append(name)
    labels.sort()
    return labels
