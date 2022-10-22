import tensorflow as tf
import cv2
import numpy as np
import pyautogui
import screeninfo

def screenGrabShop():
    monitor_x = screeninfo.get_monitors()[0].width
    monitor_y = screeninfo.get_monitors()[0].height

    xRatio = monitor_x/2560
    yRatio = monitor_y/1440
    yTop = int(1237 * yRatio)
    yBottom = int(1425 * yRatio)
    xStart = int(640 * xRatio)
    xWidth = int(257 * xRatio)
    xSpacing = int(268 * xRatio)

    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    images = []
    for i in range(0, 5):
        champ = image[yTop:yBottom, xStart + i * xSpacing:xStart + xWidth + i * xSpacing]
        images.append(champ)
    return images


def predictImage(image, interpreter, class_names):
    ## get image
    # img_height = 188
    # img_width = 257
    # img = tf.keras.utils.load_img(
    #     path, target_size=(img_width, img_height)
    # )
    img = image
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    # build classifier
    classify_lite = interpreter.get_signature_runner('serving_default')
    classify_lite
    predictions_lite = classify_lite(rescaling_1_input=img_array)['dense_1']
    score_lite = tf.nn.softmax(predictions_lite)


    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score_lite)], 100 * np.max(score_lite))
    )
    result = class_names[np.argmax(score_lite)]
    return result


def getLabels(labelFile):
    f = open(labelFile, 'r')
    labels = [line[0:-1] for line in f]
    return labels