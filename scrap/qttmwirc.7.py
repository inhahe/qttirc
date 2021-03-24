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
#color codes input
#maybe irc commands that use factoryinstance.serverconnection.* could just use factoryinstance.*
#[4:15am] <mrvn> void QWidget::customContextMenuRequested ( const QPoint & pos ) [signal]
#[4:17am] <mrvn> When you get that signal you have to map the pos to global coordinates, create a QMenu and exec_() it there
#[4:17am] <mrvn> And you can use listWidget.itemAt(pos)
#find out why connection process hangs sometimes after "got ident response", or set a timeout, or something.
#make a networkusers class, so we don't have to set a nick's ident/hostmask on each channel when we discover it? and maybe other reasons, related to private messages?
#change nick in nicklist on mode update - http://www.geekshed.net/2009/10/nick-prefixes-explained/
#change font to excelsior and decode irc lines from utf-8, also enlargen font sizes
#nickslist - don't let it keep a nick selected "item needs to be selectable. but you can style the qlistwidget with qss to make selected/normal appear same"


import os, sys, time
import re
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
      self.setPlainText("")
      if text.lstrip().startswith("/"):
        params = text.lstrip()[1:].split()
        if params[0].lower() == "join":
          if len(params) in (2, 3):
            self.network.factoryinstance.serverconnection.join(*params[1:])
          else:
            self.network.serverwindow.addline("* Usage: /join <channel> [key]")
        else:
          self.network.serverwindow.addline("* Command not recognized.")
      else:
        self.network.serverwindow.addline("* Nothing performed. This is not a channel or private-message window.")
    else:
      QTextEdit.keyPressEvent(self, event)
      
      
class ChannelInputQTextEdit(QTextEdit):
  def __init__(self, channel):
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
            self.channel.network.factoryinstance.serverconnection.join(*params[1:])
          else:
            self.channel.channelwindow.addline("* Usage: /join <channel> [key]")
        else:
          self.channel.channelwindow.addline("* Command not recognized.")
      else:
        self.channel.network.factoryinstance.serverconnection.msg(self.channel.channelname, text)
        for msg in text.split(r"\n"):
          self.channel.channelwindow.addline("<%s> %s" % (self.channel.network.factoryinstance.serverconnection.nickname, msg))
    else:
      QTextEdit.keyPressEvent(self, event)
      
class ChannelNicks(QTextEdit):
  def __init__(self):
    QTextEdit.__init__(self)
    

class ServerConnection(irc.IRCClient):
  nickname = "qttmwirc"
  
  def signedOn(self):
    #print "signed on"
    self.factoryinstance.network.serverwindow.addline("* You are now signed on.")
  
  def IRCcommand(self, command, prefix, params): #relies on a change to irc.py
    #print [command, prefix, params]
    if command not in ("PING", "PONG"):
      self.factoryinstance.network.serverwindow.addline(repr([command, prefix, params])) #debug 
  
  def privmsg(self, fromhostmask, target, msg):
    target_lower = target.lower()
    if target_lower in self.factoryinstance.network.channels:
      channel = self.factoryinstance.network.channels[target_lower]
      nick, ident, host = splithostmask(fromhostmask)
      self.factoryinstance.network.channels[target_lower].channelwindow.addline("<%s> %s" % (nick, msg))
      #if nick.lower() in channel.users: #if it's not there it's a bug anyway
      user = channel.users[nick.lower()]
      user.nick = nick
      user.ident = ident
      user.host = host
  
  def userJoined(self, hostmask, channelname): #relies on a change to irc.py
    nick, ident, host = splithostmask(hostmask)
    user = ChannelUser(nick=nick, ident=ident, host=host)
    channel = self.factoryinstance.network.channels[channelname.lower()]
    channel.users[nick.lower()] = user
    item = NickItem(nick, user)
    user.item = item
    channel.channelwindow.nickslist.addItem(item) 
 
  def userLeft(self, hostmask, channelname):
    nick, ident, host = splithostmask(hostmask)
    nick_lower = nick.lower()
    channel = self.factoryinstance.network.channels[channelname.lower()]
    nickslist = channel.channelwindow.nickslist
    nickslist.takeItem(nickslist.row(channel.users[nick_lower].item))
    del channel.users[nick.lower()]
    
  def joined(self, channelname):
    channelname_lower = channelname.lower()
    channel = Channel(channelname, self.factoryinstance.network)
    channelwindow = ChannelWindow(channel, self.factoryinstance.network)
    channel.channelwindow = channelwindow
    self.factoryinstance.network.channels[channelname_lower] = channel
    app.processEvents()
    sizes = channelwindow.splitter.sizes()
    channelwindow.splitter.setSizes([sum(sizes)-150, 150])
    #print "sizes 2:", self.factory.channels[channelname].channelwindow.splitter.sizes()
  
  def irc_RPL_NAMREPLY(self, prefix, params):
    channelname_lower = params[2].lower()
    for nick in params[3].split():
      nmo = re.match(r"([^a-zA-Z_[\]{}^`|]*).*", nick) #numbers and - can't be first character of a nick
      np = nick[:nmo.end(1)]
      nwp = nick[nmo.end(1):]
      nwp_lower = nwp.lower()
      user = ChannelUser(nwp, prefix=np)
      channel = self.factoryinstance.network.channels[channelname_lower]
      channel.users[nwp_lower] = user
      #self.factoryinstance.channels[channelname_lower].channelwindow.nickslist.insertHtml(nick + "<br>")
      item = channel.channelwindow.nickslist.addItem(NickItem(nick, user))
      channel.users[nwp_lower].item = item
      
class ServerFactory(protocol.ClientFactory):
  def __init__(self):
    pass
    
  def buildProtocol(self, addr):
      p = ServerConnection()
      self.serverconnection = p
      p.factoryinstance = self
      return p

  def clientConnectionLost(self, connector, reason):
      """If we get disconnected, reconnect to server."""
      self.serverconnection = None
      self.network.serverwindow.addline("* Disconnected. Reconnecting...")
      connector.connect()

  def clientConnectionFailed(self, connector, reason):
      #print "connection failed:", reason
      self.serverconnection = None
      self.network.serverwindow.addline("* Connection failed.") #todo: add reason
      reactor.stop()

class MainWindow(QWidget): 
    def __init__(self): 
        QWidget.__init__(self) 
        self.setWindowTitle("qttmwirc")         
    def closeEvent(self, event):
      reactor.stop() #todo: try / except. find out what the exception is when the reactor isn't already running. 
      
class ServerWindow(QWidget):
  def __init__(self, network):
    QWidget.__init__(self)
    self.network = network
    tab_widget.addTab(self, network.config["name"])
    self.textwindow = QTextEdit(self)
    self.textwindow.setReadOnly(True)
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
  def addline(self, *args):
    flag = False
    for arg in args:
      if flag:
        self.textwindow.insertHtml(arg)
      else:
        self.textwindow.insertPlainText(arg)
      flag = not flag
    self.textwindow.insertHtml("<br>")
      
class Channel:
  def __init__(self, channelname, network):
    self.channelname = channelname
    self.users = {}
    self.network = network
  def adduser(nick, prefix=None, hostmask=None):
    self.users[nick] = ChannelUser(nick, prefix, hostmask)
    self.channelwindow.nickslist.setHtml("<br>".join(sorted(self.users.keys()))) #fortunately nicks can't have < or > in them. if i weren't lazy i would replace them anyway with &lt or whatever (assuming pyqt even supports that)
    
class ChannelUser:
  def __init__(self, nick, prefix=None, host=None, ident=None):
    self.prefix = prefix
    self.host = host
    self.nick = nick
    self.ident = ident
      
class ChannelWindow(QWidget):
  def __init__(self, channel, network):
    QWidget.__init__(self)
    self.tab_index = tab_widget.addTab(self, channel.channelname)
    tab_widget.setCurrentIndex(self.tab_index)
    self.splitter = QSplitter(self)
    self.nickslist = QListWidget(self)
    self.nickslist.setSortingEnabled(True)
    #self.nickslist.setReadOnly(True) #in case we change this back to a QTextEdit
    self.textwindow = QTextEdit(self)
    self.textwindow.setReadOnly(True)
    self.splitter.addWidget(self.textwindow)
    self.splitter.addWidget(self.nickslist)
    self.network = network
    self.vlayout = QVBoxLayout(self)
    self.vlayout.setContentsMargins(0, 0, 0, 0)
    self.vlayout.addWidget(self.splitter)
    self.editwindow = ChannelInputQTextEdit(channel)
    self.vlayout.addWidget(self.editwindow)
    nickswidth = self.nickslist.width()
    textwidth = self.textwindow.width()
    self.editwindow.setFixedHeight(40)
    self.editwindow.setFocus()
  
  def addline(self, *args):
    flag = False
    for arg in args:
      if flag:
        self.textwindow.insertHtml(arg)
      else:
        self.textwindow.insertPlainText(arg)
      flag = not flag
    self.textwindow.insertHtml("<br>")

class NickItem(QListWidgetItem):
  def __init__(self, nick, user):
    QListWidgetItem.__init__(self, nick)
    self.user = user
  def __lt__(self, other):
    return self.text().toLower() < other.text().toLower() #todo: is @ < +? 
  
class Network:
  def __init__(self, factoryinstance, config):
    self.factoryinstance = factoryinstance
    self.config = config
    self.channels = {}

def splithostmask(hostmask):
  nick, rest = hostmask.split("!", 1)
  ident, host = rest.split("@", 1)
  return nick, ident, host

config = json.load(open("qttmwirc.conf.json"))

from twisted.internet import reactor

app = QApplication([])

networks = []
    
mainwindow = MainWindow()
mainwindow.showMaximized()

tab_widget = QTabWidget()
vbox = QVBoxLayout() 
vbox.addWidget(tab_widget)
vbox.setContentsMargins(0, 0, 0, 0)
mainwindow.setLayout(vbox)    

for network_config in config["networks"]:
  factoryinstance = ServerFactory()
  network = Network(factoryinstance, network_config)
  serverwindow = ServerWindow(network)
  factoryinstance.network = network
  network.serverwindow = serverwindow
  networks.append(network)
  reactor.connectTCP(network_config["servers"][0][0], network_config["servers"][0][1], factoryinstance) 

reactor.run()
