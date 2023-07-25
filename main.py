"""The main file of the bot."""
import os
import Utils.grabChampImages as gci
import time
import Utils.interface as interface
from game import Game
from pynput import keyboard
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def main():
    """Run the bot."""
    print('\n\nrunning...')
    window = interface.main()
    # ################################ MAIN LOOP ############################ #
    # on shop update
    game = Game(window)

# def imagePredict(labels, interpreter):
#     """Predict the champ in an image."""
#     images = gci.screenGrabShop()
#     for image in images:
#         gci.predictImage(image, interpreter, labels)

if __name__ == "__main__":
    time.sleep(5)
    main()
