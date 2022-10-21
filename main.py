from os import path
import tensorflow as tf
# import keras I think this line was the issue
from tensorflow import keras
from keras import layers
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def main():
    print('\n\nrunning...')
    model = keras.models.load_model(path.join(os.getcwd(), 'my_model'))  # type: ignore
    # model.predict()


if __name__ == "__main__":
    main()
