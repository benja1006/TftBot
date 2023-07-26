import sys
import screen_coords

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pynput.keyboard import Key, Listener, KeyCode
import pyautogui


global opc
opc = 1

global target_champs
target_champs = ['a','b']

global curr_shop
curr_shop = ['a', 'b', 'EMPTY', 'EMPTY', 'EMPTY']

class CustomWindow(QMainWindow):
    keyPressed = pyqtSignal(KeyCode)
    
    def __init__(self, app, sc, parent=None):
        super().__init__(parent)
        self.listener = Listener(on_release=self.on_release)
        self.app = app
        self.sc = sc
        self.target_champs = []
        self.curr_shop = []

    def on_release(self, key):
        try: 
            self.keyPressed.emit(key)
        except:
            return
        
        if key.char == 'd':
            # Champ Checking Occurs Here
            global curr_shop
            curr_shop = ['a', 'EMPTY', 'EMPTY', 'b', 'EMPTY']

            self.update()

    def stop_monitoring(self):
        self.listener.stop()

    def start_monitoring(self):
        self.listener.start()

    def paintEvent(self, event=None):
        # Window painter
        painter = QPainter(self)
        painter.setOpacity(0)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))   
        painter.drawRect(self.rect())
        
        # Box painter
        painter1 = QPainter(self)
        painter1.setOpacity(opc)
        painter1.setPen(QPen(Qt.red,  5, Qt.SolidLine))


        for idx, champ in enumerate(self.curr_shop):
            if champ in self.target_champs:
                spacing = round(screen_coords.CHAMP_SPACING * self.sc)
                x = round(screen_coords.CHAMP_LEFT * self.sc)
                y = round(screen_coords.CHAMP_TOP * self.sc)
                height = round((screen_coords.CHAMP_BOT * self.sc) - (screen_coords.CHAMP_TOP * self.sc))
                width = round((screen_coords.CHAMP_RIGHT * self.sc) - (screen_coords.CHAMP_LEFT * self.sc))
                painter1.drawRect(x + (spacing * idx), y, width, height)

def main(sc):
    app = QApplication(sys.argv)
    # Create the main window
    window = CustomWindow(app, sc)
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setAttribute(Qt.WA_NoSystemBackground, True)
    window.setAttribute(Qt.WA_TranslucentBackground, True)
    window.start_monitoring()

    # Create the button
    pushButton = QPushButton(window)
    pushButton.setGeometry(QRect(240, 190, 90, 31))
    pushButton.setText("Finished")
    pushButton.clicked.connect(app.quit)

    # Center the button
    qr = pushButton.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    pushButton.move(qr.topLeft())

    # Run the application
    window.showFullScreen()

    # Enable Always On Top from Power Toys
    '''
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("winleft")
    pyautogui.press("t")
    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("winleft")
    '''
    # app.exec_()
    # sys.exit(app.exec_())
    return window

if __name__ == "__main__":
    main(1)
