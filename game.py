"""Handles the gameplay."""
import win32gui
from window import Window
import game_functions
import Utils.grabChampImages as gci
import tensorflow as tf
import os
import re


class Game:
    """The game class."""

    def __init__(self, interface):
        """Innitiate instance variables and find the TFT window."""
        self.round = "0-0"
        self.roundStatus = "Loading Screen"
        self.found_window = False
        self.interface = interface
        self.dPressed = False
        print('Loading Model...')
        TF_MODEL_FILE_PATH = 'model.tflite'
        self.interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
        self.labels = gci.getLabels(os.path.join(os.getcwd(), 'labels.txt'))
        print("\n[!] Searching for game window")
        while not self.found_window:
            print("  Did not find window, trying again...")
            win32gui.EnumWindows(self.findWindow, None)
            game_functions.update_tk_loop(self.interface.tk, 1, self.dPressed)
        self.loading_screen()

    def findWindow(self, hwnd, extra):
        """Find the League window."""
        if "League of Legends (TM) Client" not in win32gui.GetWindowText(hwnd):
            return
        rect = win32gui.GetWindowRect(hwnd)

        x_pos = rect[0]
        y_pos = rect[1]
        width = rect[2] - x_pos
        height = rect[3] - y_pos

        if width < 200 or height < 200:
            return

        print(f"  Window {win32gui.GetWindowText(hwnd)} found")
        print(f"    Location: ({x_pos}, {y_pos})")
        print(f"    Size:     ({width}, {height})")
        self.Window = Window(x_pos, y_pos, width, height)
        self.found_window = True

    def loading_screen(self):
        """Wait for the loading screen to end."""
        print('Waiting for loading screen')
        # while game_functions.get_round(self.Window) != "1-1":
        while game_functions.get_round(self.Window) == "":
            game_functions.update_tk_loop(self.interface.tk, 1, self.dPressed)
            self.dPressed = False
        print('Loading screen over, currently round:' +
              game_functions.get_round(self.Window))
        self.game_loop()

    def game_loop(self):
        """Run the main functions of the bot when in game."""
        # get current desired champs

        while True: #FIXME Really need to do something better here.
            self.wanted_champs = self.interface.getList()
            self.round = game_functions.get_round(self.Window)
            if self.round not in ["0-0", "1-1", "2-4", "3-4", "4-4", "5-4", "6-4",
                                  "7-4"]:
                # we are in a regular round
                curr_champs = game_functions.get_curr_champs(self.Window,
                                                             self.interpreter,
                                                             self.labels)
                for champ, idx in curr_champs:
                    if champ in self.wanted_champs:
                        # draw outline around index on overlay
                        print("Buy " + champ + " in the " + str(idx) + "position")
            game_functions.update_tk_loop(self.interface.tk, 1, self.dPressed)
            self.dPressed = False

    def on_press(self, key):
        """Update dPressed when d is pressed."""
        if not hasattr(key, 'char'):
            return
        if key.char == 'd':
            print('D Pressed')
            self.dPressed = True

    def on_release(self, key):
        """Do nothing when a key is released."""
        return
