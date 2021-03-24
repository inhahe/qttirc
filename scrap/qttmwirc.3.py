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

class MainWindow(QWidget): 
    def __init__(self): 
        QWidget.__init__(self) 
        # setGeometry(x_pos, y_pos, width, height) 
        #self.setGeometry(250, 150, 400, 300) 
        self.setWindowTitle("QTTMWIRC")         
         
        tab_widget = QTabWidget() 
        tab1 = QWidget() 
        tab2 = QWidget() 
         
        tab_widget.addTab(tab1, "page1") 
        tab_widget.addTab(tab2, "page2")
        
        # put a button on tab1 (page1)
        #btn_hello1 = QPushButton("Hello page1", tab1)
        #btn_hello1.move(10, 10)
        # put a button on tab2 (page2)
        #btn_hello2 = QPushButton("Hello page2", tab2)
        #btn_hello2.move(10, 10)
        # layout manager
        vbox = QVBoxLayout()
        vbox.addWidget(tab_widget)         
        self.setLayout(vbox)      
        # optionally create layout for each page
        p1_vbox = QVBoxLayout(tab1)
        #p1_vbox.addWidget(btn_hello1) 
        p2_vbox = QVBoxLayout(tab2)
        
class ServerWindow(QWidget, tab_bar, network):
  def __init__(self, tab_bar):
    QWidget.__init__(self)
    tab_bar.addTab(self, network["name"])

config = json.load(open("qttmwirc.conf.json"))

from twisted.internet import reactor

open_network_windows = []
networks = {}
pages = {}

for network in config["networks"]:
  page = ServerWindow(network, )
  instance = qttmwirc_factory()
  networks[network["name"]] = instance
  #reactor.connectTCP(network["servers"][0][0], network["servers"][0][1], instance)
    
app = QApplication([])
#mainwindow = qttmwirc_gui(reactor)

mainwindow = MainWindow()
mainwindow.showMaximized()

reactor.run()
