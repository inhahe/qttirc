#todo:
#cycle through servers on connection fail
#cycle through nicks on nick taken / invalid nick
#copy.deepcopy config[network] when passing to factory
#find out how to make config class
#print connection dialog in server window
#how do i show the server messages that are in green in mIRC
#add scrollbar to server window
#keep scrollback below x lines
#better handling of MODE command from server
#when joining, read names list
#don't show names list or end of names list in window
#fix joining so it actually makes a new tab like it should.
#hook scrollback of channel windows to bottom
#make new tab active tab when a new tab is made
#detect if shift was pressed while enter was pressed and if so don't process yet
#identd
#make input qtextedit active when window loads

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

#if multiple lines inputted, detect if each line starts with "/" and run the command if it does?
class ServerInputQTextEdit(QTextEdit):
  def __init__(self, network):
    QTextEdit.__init__(self)
    self.network = network
  def keyPressEvent(self, event):
    if event.key() == Qt.Key_Return:
      
      text = str(self.toPlainText())
      #print "text:", text #debug
      self.setPlainText("")
      if text.lstrip().startswith("/"):
        params = text.lstrip()[1:].split()
        if params[0].lower() == "join":
          if len(params) in (2, 3):
            self.network["connection"].serverconnection.join(*params[1:])
          else:
            self.network["serverwindow"].addline("* Usage: /join <channel> [key]")
        else:
          self.network["serverwindow"].addline("* Command not recognized.")
      else:
        self.network["serverwindow"].addline("* Nothing performed. This is not a channel or private-message window.")
    else:
      QTextEdit.keyPressEvent(self, event)
      
class ChannelNicks(QTextEdit):
  def __init__(self):
    QTextEdit.__init__(self)
    

class ServerConnection(irc.IRCClient):
  nickname = "qttmwirc"
  def signedOn(self):
    #print "signed on"
    #self.factory.serverwindow.addline("signed on<br/>")
    pass
  def IRCcommand(self, command, prefix, params):
    #print [command, prefix, params]
    if command not in ("PING", "PONG"):
      self.factory.serverwindow.addline(repr([command, prefix, params])) #debug 
  def privmsg(self, user, channel, msg):
    pass
    #print "privmsg:", [user, channel, msg]#debug
  def joined(self, channel):
    self.factory.channels[channel] = Channel(channel)
    self.factory.channels[channel].window = ChannelWindow(channel)
    print "sizes 1:", self.factory.channels[channel].window.splitter.sizes()
    app.processEvents()
    print "sizes 2:", self.factory.channels[channel].window.splitter.sizes()
  def irc_NAMREPLY(prefix, params):
    channel = params[2].lower()
    for nick in params[3].split():
      nmo = re.match(r"([^a-zA-Z_[\]{}^`|]*).*", nick) #numbers and - can't be first character of a nick
      np = nick[:nmo.end(1)]
      nwp = nick[nmo.end(1):]
      self.factory.channels[channel].users[nwp.lower()] = ChannelUser(nick, prefix=np)
      
class ServerFactory(protocol.ClientFactory):
  def __init__(self, serverwindow):
      self.serverwindow = serverwindow
      self.channels = {}
    
  def buildProtocol(self, addr):
      p = ServerConnection()
      self.serverconnection = p
      p.factory = self
      return p

  def clientConnectionLost(self, connector, reason):
      """If we get disconnected, reconnect to server."""
      self.serverconnection = None
      connector.connect()

  def clientConnectionFailed(self, connector, reason):
      #print "connection failed:", reason
      self.serverconnection = None
      self.serverwindow.addline("Connection failed.")
      reactor.stop()

class MainWindow(QWidget): 
    def __init__(self): 
        QWidget.__init__(self) 
        # setGeometry(x_pos, y_pos, width, height) 
        #self.setGeometry(250, 150, 400, 300) 
        self.setWindowTitle("qttmwirc")         
    def closeEvent(self, event):
      reactor.stop()
      
class ServerWindow(QWidget):
  def __init__(self, network):
    QWidget.__init__(self)
    tab_widget.addTab(self, network["name"])
    self.textwindow = QTextEdit(self)
    self.textwindow.setReadOnly(True)
    self.network = network
    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.addWidget(self.textwindow)
    self.editwindow = ServerInputQTextEdit(network) #self, network
    self.layout.addWidget(self.editwindow)
    #sizepolicy = QSizePolicy()
    #sizepolicy.setVerticalPolicy()
    #self.editwindow.setSizePolicy(sizepolicy)
    self.editwindow.setFixedHeight(40)
  def addline(self, line):
    self.textwindow.insertHtml(line + "<br>")
      
class Channel:
  def __init__(self, channel):
    self.name = channel
    self.users = {}
    
class ChannelUser:
  def __init__(self, nick, prefix=None, hostmask=None):
    self.prefix = prefix
    self.hostmask = hostmask
    
class ChannelWindow(QWidget):
  def __init__(self, channel):
    QWidget.__init__(self)
    self.tab_index = tab_widget.addTab(self, channel)
    tab_widget.setCurrentIndex(self.tab_index)
    self.splitter = QSplitter(self)
    self.nickslist = QTextEdit(self)
    self.nickslist.setReadOnly(True)
    self.textwindow = QTextEdit(self)
    self.textwindow.setReadOnly(True)
    self.splitter.addWidget(self.textwindow)
    self.splitter.addWidget(self.nickslist)
                                          #resize app and see if it behaves correctly. if not try setting stretch factor of nicks list to 0.
    self.network = network
    self.vlayout = QVBoxLayout(self)
    self.vlayout.setContentsMargins(0, 0, 0, 0)
    self.vlayout.addWidget(self.splitter)
    self.editwindow = QTextEdit(self)
    self.vlayout.addWidget(self.editwindow)
    nickswidth = self.nickslist.width()
    textwidth = self.textwindow.width()
    print "nicks/text widths:", nickswidth, textwidth #debug
    width = self.width() #why doesn't self.splitter.width() work?
    #self.splitter.setSizes([width-30, 30]) #todo: make nicks list size proportional to font size. also, make it actually work with the size specified.      
    #self.nickslist.setFixedWidth(150)
    self.nickslist.resize(100, self.nickslist.height())
    self.splitter.setStretchFactor(self.splitter.indexOf(self.nickslist), 0)
    nickswidth = self.nickslist.width()
    textwidth = self.textwindow.width()
    print "nicks/text widths:", nickswidth, textwidth #debug
    print "splitter width:",self.splitter.width()
    print "splitter.geometry width:", self.splitter.geometry().width()
    #sizepolicy = QSizePolicy()
    #sizepolicy.setVerticalPolicy()
    #self.editwindow.setSizePolicy(sizepolicy)
    self.editwindow.setFixedHeight(40)
  def addline(self, line):
    self.textwindow.insertHtml(line)

config = json.load(open("qttmwirc.conf.json"))

from twisted.internet import reactor

app = QApplication([])

open_network_windows = []
networks = config["networks"]
    
mainwindow = MainWindow()
mainwindow.showMaximized()

tab_widget = QTabWidget()
vbox = QVBoxLayout()  
vbox.addWidget(tab_widget)
vbox.setContentsMargins(0, 0, 0, 0)
mainwindow.setLayout(vbox)      

for network in networks:
  serverwindow = ServerWindow(network)
  connection = ServerFactory(serverwindow)
  #print dir(connection)
  network["connection"] = connection
  network["serverwindow"] = serverwindow
  open_network_windows.append(serverwindow)
  reactor.connectTCP(network["servers"][0][0], network["servers"][0][1], connection)

reactor.run()
