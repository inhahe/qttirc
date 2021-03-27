#!/usr/bin/python3
"""
Prototype of a window with twisted
"""

import sys
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
        QAction, QActionGroup, QApplication, QFrame, QLabel, QMainWindow,
        QMenu, QMessageBox, QSizePolicy, QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

    def closeEvent(self, event):
         QCoreApplication.instance().quit()

if __name__ == '__main__':

    def stop():
        print("Stop")
        if reactor.running:
            reactor.stop()

    app = QApplication(sys.argv)
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor
    window = MainWindow()
    window.show()
    app.lastWindowClosed.connect(stop)
    reactor.run()
