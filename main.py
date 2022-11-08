from os import path
import tensorflow as tf
# import keras I think this line was the issue
from tensorflow import keras
from keras import layers
import os
import Utils.grabChampImages as gci
import time
import interface
from game import Game
import pynput as keyboard


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def main():
    print('\n\nrunning...')
    window = interface.main()
    # ################################ MAIN LOOP ############################ #
    # on shop update
    game = Game(window)
    with keyboard.Listener(
            on_press=game.on_press,
            on_release=game.on_release) as listener:
        listener.join()


def imagePredict(labels, interpreter):
    images = gci.screenGrabShop()
    for image in images:
        gci.predictImage(image, interpreter, labels)


if __name__ == "__main__":
    time.sleep(5)
    main()
