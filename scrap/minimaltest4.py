class ServerFactory(protocol.ReconnectingClientFactory):
 
  def __init__(self, nickname="qttwirc"):
    self.nickname = nickname
    
  def buildProtocol(self, addr):
    p = ServerConnection()
    self.serverconnection = p
    p.nickname = self.nickname
    self.resetDelay()
    return p
  
app = QApplication(sys.argv)
import qt5reactor
qt5reactor.install()
from twisted.internet import reactor

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QTextEdit

def addline(window, arg): 
  window.textwindow.insertPlainText(arg)
  window.textwindow.insertHtml("<br>")
  window.textwindow.moveCursor(QTextCursor.End) 
  scrollbar = window.textwindow.verticalScrollBar()
  scrollbar.setValue(scrollbar.maximum())

class MainWindow(QMainWindow):
  
  def __init__(self):
    QMainWindow.__init__(self)
    self.vbox = QVBoxLayout() 
    self.vbox.setContentsMargins(0, 0, 0, 0)
    self.textwindow = QTextEdit(self)
    self.layout.addWidget(self.textwindow)
    self.showMaximized()
    
  def closeEvent(self, event):
    QCoreApplication.instance().quit()
    
reactor.run()
  
import irc
from twisted.internet import protocol

class ServerConnection(irc.IRCClient):
  
  def signedOn(self):
    #print "signed on"
    addline(mainwin, "* You are now signed on.")
    
  def clientConnectionFailed(self, connector, reason):
    addline(mainwin, "* Connection failed.")
    
  def clientConnectionLost(self, connector, reason):
    addline(mainwin, "* Connection lost.")

mainwin = MainWindow()
conn = reactor.connectTCP("irc.undernet.org", 6667, server)

    
