"""Handles the gameplay."""
import win32gui
from Utils.window import Window
import game_functions
import Utils.grabChampImages as gci
import tensorflow as tf
import os
import re
import keyboard
import sys
import overlay


class Game:
    """The game class."""

    def __init__(self, interface):
        """Innitiate instance variables and find the TFT window."""
        self.round = "0-0"
        self.roundStatus = "Loading Screen"
        self.found_window = False
        self.interface = interface
        self.dPressed = False
        keyboard.add_hotkey('ctrl+q', self.quit)
        keyboard.add_hotkey('d', self.on_d_press)

        print('Loading Model...')
        TF_MODEL_FILE_PATH = 'model.tflite'
        self.interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
        self.labels = gci.getLabels(os.path.join(os.getcwd(), 'Utils', 'labels.txt'))
        print("\n[!] Searching for game window")
        while not self.found_window:
            print("  Did not find window, trying again...")
            win32gui.EnumWindows(self.findWindow, None)
            game_functions.update_tkQT_loop(self.interface.tk, 1, self.dPressed)
            self.check_tk_closed()
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
        sc = width / 2560
        self.overlay = overlay.main(sc)
        print("running main")

    def loading_screen(self):
        """Wait for the loading screen to end."""
        print('Waiting for loading screen')
        # while game_functions.get_round(self.Window) != "1-1":
        while game_functions.get_round(self.Window) == "":
            game_functions.update_tkQT_loop(self.interface.tk, 1, self.dPressed)
            self.dPressed = False
        print('Loading screen over, currently round:' +
              game_functions.get_round(self.Window))
        self.game_loop()

    def game_loop(self):
        """Run the main functions of the bot when in game."""
        # get current desired champs

        while True: #FIXME Really need to do something better here.
            self.wanted_champs = self.interface.getList()
            new_round = game_functions.get_round(self.Window)
            if new_round != self.round:
                self.updated = True
                self.round = new_round
            if self.round not in ["0-0", "1-1", "2-4", "3-4", "4-4", "5-4", "6-4",
                                  "7-4"]:
                # we are in a regular round

                # now check if the round has changed or d has been pressed
                if self.updated:

                    curr_champs = game_functions.get_curr_champs(self.Window,
                                                                self.interpreter,
                                                                self.labels)
                    self.updated = False
                self.overlay.curr_shop = curr_champs
                self.overlay.target_champs = self.wanted_champs

            win32gui.EnumWindows(self.check_window_closed, None)
            # if self.game_over:
            #     self.end_game()
            game_functions.update_tkQT_loop(self.interface.tk, 1, self.dPressed, self.overlay)
            if self.dPressed:
                self.updated = True
            self.dPressed = False
            self.check_tk_closed()


    def check_window_closed(self, hwnd, extra):
        # print(win32gui.GetWindowText(hwnd))
        if "League of Legends (TM) Client" not in win32gui.GetWindowText(hwnd):
            self.game_over = True


    # def end_game(self):
    #     """Reset system and return to Loading Screen status."""
    #     print('Game has ended. Resetting bot and waiting for next game to '
    #           'begin.')
    #     self.round = "0-0"
    #     self.roundStatus = "Loading Screen"
    #     self.found_window = False
    #     self.dPressed = False
    #     self.interface.reset()
    #     self.overlay.app.quit()
    #     print("\n[!] Searching for game window")
    #     while not self.found_window:
    #         print("  Did not find window, trying again...")
    #         win32gui.EnumWindows(self.findWindow, None)
    #         game_functions.update_tkQT_loop(self.interface.tk, 1, self.dPressed)
    #     self.loading_screen()

    def quit(self):
        sys.exit()
    
    def on_d_press(self):
        self.dPressed = True
        print("Pressed D")
    
    def check_tk_closed(self):
        if self.interface.closed:
            print('Interface has been closed. Quitting...')
            self.quit()