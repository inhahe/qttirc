
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

if __name__ == "__main__":

    app = QApplication(sys.argv)

    class SampleGUIClientWindow(QMainWindow):
        def __init__(self, parent=None):
            super(SampleGUIClientWindow, self).__init__(parent)

        def closeEvent(self, event):
          reactor.stop()
          app.exit()
          sys.exit()
          pass

    import qt4reactor
    qt4reactor.install()
    
    from twisted.internet import reactor

    MainWindow = SampleGUIClientWindow()
    MainWindow.show()

    sys.exit(app.exec_())
    reactor.runReturn()