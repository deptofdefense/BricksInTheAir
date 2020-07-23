from PyQt5.QtCore import Qt # needed for gui
from PyQt5.QtGui import *  # needed for gui
from PyQt5.QtWidgets import * # needed for gui

import sys # needed for gui

import time # needed for sleep
import threading # needed for threads

class GameDisplay(QMainWindow):
    ''' Custom Class to handle the game overlay window '''

    def __init__(self, CFG):
        super().__init__()
        self.cfg = CFG

        # set the title
        self.setWindowTitle("Text Overlay Window")

        # makes the background transparent when xcompmgr is running
        self.setAttribute(Qt.WA_TranslucentBackground)

        # setting  the geometry of window
        self.setGeometry(0, 0, self.cfg["display"]["width"], self.cfg["display"]["height"])

        # Command Label
        self.cmdLabel = QLabel("cmdLabel", self)
        self.cmdLabel.setStyleSheet("color: rgb(251, 0, 255);")
        self.cmdLabel.setText("")
        self.cmdLabel.setFont(QFont('Arial', 20))
        self.cmdLabel.resize(self.cfg["display"]["width"], self.cfg["display"]["height"])
        self.cmdLabel.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        # UserList Label
        self.lstLabel = QLabel("lstLabel", self)
        self.lstLabel.setStyleSheet("color: rgb(251, 0, 255);")
        self.lstLabel.setText("Active User List (limit {}): ".format(self.cfg["cue"]["limit"]))
        self.lstLabel.setFont(QFont('Arial', 20))
        self.lstLabel.resize(self.cfg["display"]["width"], self.cfg["display"]["height"])
        self.lstLabel.setAlignment(Qt.AlignRight)

        # show all the widgets
        self.show()

    def dispCmd(self, cmdMsg):
        ''' Causes a string representing the command message to be displayed on the bottom of the screen '''

        self.cmdLabel.setText(str(cmdMsg))
        #self.show
        time.sleep(5)
        self.cmdLabel.setText("")
        self.cmdLabel.update()
        #self.show

    def dispUser(self, userMsg):
        ''' Updates the user list '''

        self.lstLabel.setText("Active User List (limit {})\n{}".format(self.cfg["cue"]["limit"], userMsg))
        self.lstLabel.update()

class DisplayManager():
    ''' Custom class for managing the display '''

    def __init__(self, cfg):
        self.cfg = cfg

    def __startDisplayThread(self):
        ''' private class for starting the display as a separate thread '''

        #print("test")

        # create pyqt5 app
        App = QApplication(sys.argv)

        # create the instance of our Window
        self.display = GameDisplay(self.cfg)

        # start the app
        sys.exit(App.exec())

    def startDisplay(self):
        ''' Starts the game overlay '''
        threading.Thread(target=self.__startDisplayThread, daemon=True).start()
        time.sleep(1)

    def updateUserList(self, userMsg):
        ''' public interface for updating the user list '''
        self.display.dispUser(userMsg)

    def updateCmdMsg(self, cmdMsg):
        ''' public interface for updating the command message '''
        threading.Thread(target=self.display.dispCmd, args=(cmdMsg, ), daemon=True).start()
