from os import path
import tensorflow as tf
# import keras I think this line was the issue
from tensorflow import keras
from keras import layers
import os
import Utils.grabChampImages as gci
import time
import interface


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def main():
    TF_MODEL_FILE_PATH = 'model.tflite'
    print('\n\nrunning...')
    interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
    labels = gci.getLabels(os.path.join(os.getcwd(), 'labels.txt'))
    window = interface.main()
    ################################# MAIN LOOP ################################
    # on shop update




def imagePredict(labels, interpreter):
    images = gci.screenGrabShop()
    for image in images:
        gci.predictImage(image, interpreter, labels)



if __name__ == "__main__":
    time.sleep(5)
    main()
