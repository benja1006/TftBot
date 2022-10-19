import my_model
import tensorflow as tf
import keras
from tensorflow import keras
from keras import layers
import os
from os import path

def main():
    print('\n\nrunning...')
    model = keras.models.load_model(path.join(os.getcwd(), 'my_model'))


if __name__ == "__main__":
    main()
