'''Handles the gameplay'''
import win32gui
import time
from window import Window

class Game:
    def __init__(self):
        self.round = 0.
        self.roundStatus = "Loading Screen"
        self.found_window = False
        print("\n[!] Searching for game window")
        while not self.found_window:
            print("  Did not find window, trying again...")
            win32gui.EnumWindows(self.findWindow, None)
            time.sleep(1)
        self.loading_screen()

    def findWindow(self, hwnd, extra):
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
