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
#see if irc.py is strip()ping the parameters from the server
#if all alternative nicks are in use, popup a dialog asking for a nick
#input history 

#[4:15am] <mrvn> void QWidget::customContextMenuRequested ( const QPoint & pos ) [signal]
#[4:17am] <mrvn> When you get that signal you have to map the pos to global coordinates, create a QMenu and exec_() it there
#[4:17am] <mrvn> And you can use listWidget.itemAt(pos)


import os, sys, time
import re
#import Queue
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
            self.network["factoryinstance"].serverconnection.join(*params[1:])
          else:
            self.network["serverwindow"].addline("* Usage: /join <channel> [key]")
        else:
          self.network["serverwindow"].addline("* Command not recognized.")
      else:
        self.network["serverwindow"].addline("* Nothing performed. This is not a channel or private-message window.")
    else:
      QTextEdit.keyPressEvent(self, event)
      
      
class ChannelInputQTextEdit(QTextEdit):
  def __init__(self, channel, network):
    QTextEdit.__init__(self)
    self.channel = channel
  def keyPressEvent(self, event):
    if event.key() == Qt.Key_Return and not (event.modifiers() and Qt.ShiftModifier):
      text = str(self.toPlainText())
      self.setPlainText("")
      if text.lstrip().startswith("/"):
        params = text.lstrip()[1:].split()
        if params[0].lower() == "join":
          if len(params) in (2, 3):
            self.channel.serverconnection.join(*params[1:])
          else:
            self.channel.channelwindow.addline("* Usage: /join <channel> [key]")
        else:
          self.channel.channelwindow.addline("* Command not recognized.")
      else:
        for msg in text.split(r"\n"):
          self.channel.network["factoryinstance"].msg(self.channel.channelname, text)
          self.channel.channelwindow.addline("<%s> %s" % (self.channel.serverconnection.nickname))
    else:
      QTextEdit.keyPressEvent(self, event)
      
class ChannelNicks(QTextEdit):
  def __init__(self):
    QTextEdit.__init__(self)
    

class ServerConnection(irc.IRCClient):
  nickname = "qttmwirc"
  def signedOn(self):
    #print "signed on"
    self.factoryinstance.serverwindow.addline("* You are now signed on.")
  def IRCcommand(self, command, prefix, params):
    #print [command, prefix, params]
    if command not in ("PING", "PONG"):
      self.factoryinstance.serverwindow.addline(repr([command, prefix, params])) #debug 
  def privmsg(self, user, channelname, msg):
    print "privmsg:" [self, user, channelname, msg] #debug
    #print "privmsg:", [user, channel, msg]#debug
  def joined(self, channelname):
    channelname_lower = channelname.lower()
    channel = Channel(channelname, ChannelWindow(channelname), self)
    channel.channelwindow.network = self.factoryinstance
    self.factoryinstance.channels[channelname_lower] = channel
    app.processEvents()
    sizes = self.factoryinstance.channels[channelname_lower].channelwindow.splitter.sizes()
    self.factoryinstance.channels[channelname_lower].channelwindow.splitter.setSizes([sum(sizes)-150, 150])
    #print "sizes 2:", self.factory.channels[channelname].channelwindow.splitter.sizes()
  def irc_RPL_NAMREPLY(self, prefix, params):
    channelname_lower = params[2].lower()
    for nick in params[3].split():
      nmo = re.match(r"([^a-zA-Z_[\]{}^`|]*).*", nick) #numbers and - can't be first character of a nick
      np = nick[:nmo.end(1)]
      nwp = nick[nmo.end(1):]
      self.factoryinstance.channels[channelname_lower].users[nwp.lower()] = ChannelUser(nwp, prefix=np)
      #self.factoryinstance.channels[channelname_lower].channelwindow.nickslist.insertHtml(nick + "<br>")
      self.factoryinstance.channels[channelname_lower].channelwindow.nickslist.addItem(NickItem(nick))
      
class ServerFactory(protocol.ClientFactory):
  def __init__(self, serverwindow):
      self.serverwindow = serverwindow
      self.channels = {}
    
  def buildProtocol(self, addr):
      p = ServerConnection()
      self.serverconnection = p
      p.factoryinstance = self
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
    self.editwindow.setFocus()
  def addline(self, line):
    self.textwindow.insertHtml(line + "<br>")
      
class Channel:
  def __init__(self, channelname, channelwindow, network):
    self.channelname = channelname
    self.users = {}
    self.channelwindow = channelwindow
    self.serverconnection = network.serverconnection
    self.network = network
  def adduser(nick, prefix=None, hostmask=None):
    self.users[nick] = ChannelUser(nick, prefix, hostmask)
    self.channelwindow.nickslist.setHtml("<br>".join(sorted(self.users.keys()))) #fortunately nicks can't have < or > in them. if i weren't lazy i would replace them anyway with &lt or whatever (assuming pyqt even supports that)
    
class ChannelUser:
  def __init__(self, nick, prefix=None, hostmask=None):
    self.prefix = prefix
    self.hostmask = hostmask
    
class ChannelWindow(QWidget):
  def __init__(self, channel, network):
    QWidget.__init__(self)
    self.tab_index = tab_widget.addTab(self, channel.channelname)
    tab_widget.setCurrentIndex(self.tab_index)
    self.splitter = QSplitter(self)
    self.nickslist = QListWidget(self)
    self.nickslist.setSortingEnabled(True)
    #self.nickslist.setReadOnly(True)
    self.textwindow = QTextEdit(self)
    self.textwindow.setReadOnly(True)
    self.splitter.addWidget(self.textwindow)
    self.splitter.addWidget(self.nickslist)
    self.network = network
    self.vlayout = QVBoxLayout(self)
    self.vlayout.setContentsMargins(0, 0, 0, 0)
    self.vlayout.addWidget(self.splitter)
    self.editwindow = ChannelInputQTextEdit(channel, network)
    self.vlayout.addWidget(self.editwindow)
    nickswidth = self.nickslist.width()
    textwidth = self.textwindow.width()
    self.editwindow.setFixedHeight(40)
    self.editwindow.setFocus()
  def addline(self, line):
    self.textwindow.insertHtml(line)

class NickItem(QListWidgetItem):
  def __init__(self, item):
    QListWidgetItem.__init__(self, item)
  def __lt__(self, other):
    return self.text().toLower() < other.text().toLower() #todo: is @ < +? 
  
class Network:
  def __init__(factoryinstance, serverwindow):
    self.factoryinstance = factoryinstance
    self.serverwindow = serverwindow

config = json.load(open("qttmwirc.conf.json"))


from twisted.internet import reactor

app = QApplication([])

open_network_windows = []
config["networks"]
    
mainwindow = MainWindow()
mainwindow.showMaximized()

tab_widget = QTabWidget()
vbox = QVBoxLayout()  
vbox.addWidget(tab_widget)
vbox.setContentsMargins(0, 0, 0, 0)
mainwindow.setLayout(vbox)      

for network in config["networks"]:
  serverwindow = ServerWindow(network)
  factoryinstance = ServerFactory(serverwindow)
  network["factoryinstance"] = factoryinstance
  network["serverwindow"] = serverwindow
  open_network_windows.append(serverwindow)
  reactor.connectTCP(network["servers"][0][0], network["servers"][0][1], connection)

reactor.run()
