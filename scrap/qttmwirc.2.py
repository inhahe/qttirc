import os, sys, time
import Queue
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import json
import qt4reactor_


qt4reactor_.install()

#from twistedclient import SocketClientFactory
from twisted.words.protocols import irc
from twisted.internet import protocol


class qttmwirc_conn(irc.IRCClient):
  nickname = "qttmwirc"
  def signedOn(self):
    print "signed on"
  def privmsg(self, user, channel, msg):
    print "privmsg:", [user, channel, msg]
    
class qttmwirc_factory(protocol.ClientFactory):
  def __init__(self):
      pass
  def buildProtocol(self, addr):
      p = qttmwirc_conn()
      p.factory = self
      return p

  def clientConnectionLost(self, connector, reason):
      """If we get disconnected, reconnect to server."""
      connector.connect()

  def clientConnectionFailed(self, connector, reason):
      print "connection failed:", reason
      reactor.stop()

class qttmwirc_gui(QMainWindow):
    def __init__(self, reactor, parent=None):
        super(qttmwirc_gui, self).__init__(parent)
        self.reactor = reactor
        tab_widget = QTabWidget() 
        tab1 = QWidget() 
        tab2 = QWidget() 
         
        tab_widget.addTab(tab1, "page1") 
        tab_widget.addTab(tab2, "page2")
    def closeEvent(self, event):
      app.quit()
      reactor.stop()
      
config = json.load(open("qttmwirc.conf.json"))
  
networks = {}

from twisted.internet import reactor

for network in config["networks"]:
  instance = qttmwirc_factory()
  networks[network["name"]] = instance
  #reactor.connectTCP(network["servers"][0][0], network["servers"][0][1], instance)
        
app = QApplication(sys.argv)
tabbar = QTabWidget()
test1 = QWidget()
test2 = QWidget()

tabbar.addTab(test1, "test")
tabbar.addTab(test2, "test2")
mainwindow = qttmwirc_gui(reactor)
mainwindow.showMaximized()

reactor.run()
