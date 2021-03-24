
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

if __name__ == "__main__":

    app = QApplication(sys.argv)

    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    
    print "test"
    
    reactor.stop()
    app.quit()
    #from twisted.internet import reactor

    #MainWindow = SampleGUIClientWindow()
    #MainWindow.show()

    #sys.exit(app.exec_())
    #reactor.runReturn()