#todo:
#cycle through servers on connection fail
#copy.deepcopy config[network] when passing to factory
#find out how to make config class so that i can use .'s instead of [""]'s
#how do i show the server messages that are in green in mIRC
#keep scrollback below x lines
#identd
#if all alternative nicks are in use, popup a dialog asking for a nick
#input history 
#color codes input
#maybe irc commands that use server.serverconnection.* could just use server.*
#[4:15am] <mrvn> void QWidget::customContextMenuRequested ( const QPoint & pos ) [signal]
#[4:17am] <mrvn> When you get that signal you have to map the pos to global coordinates, create a QMenu and exec_() it there
#[4:17am] <mrvn> And you can use listWidget.itemAt(pos)
#find out why connection process hangs sometimes after "got ident response", or set a timeout, or something.
#make a networkusers class, so we don't have to set a nick's ident/hostmask on each channel when we discover it? and maybe other reasons, related to private messages?
#change nick in nicklist on mode update - http://www.geekshed.net/2009/10/nick-prefixes-explained/
#nickslist - don't let it keep a nick selected "item needs to be selectable. but you can style the qlistwidget with qss to make selected/normal appear same"
#use color for messages generated by the client (messages starting with *)
#move processing of commands to a separate function that is universal to server, channel and privmsg windows
#should channels be moved to server because they get erased as soon as it gets disconnected?
#make networks a dictionary
#change reconnectdelay so that it only applies to connecting to the same server again within x seconds after previous connect attempt 
#nick completion
#use fixedsys for ascii characters and excelsior for unicode. this could be a problem since excelsior sizes are different from fixedsys sizes. (e.g. 7 in fixedsys is 10 in excelsior.)
#group new channel tabs with the correct server tabs
#update user.ident, user.host, and MessageWindow for all connections having the same network name? 
#can we 'import irc' to use our local, modified copy instead of 'from twisted.words.protocols import irc'?
#ctrl-tab and ctrl-shift-tab to switch between tabs. ctrl-f4 to part a channel
#change colors of tab labels if new messages in channels
#beep/change colors of tab labels if self.nickname mentioned in channel
#command to beep if new message in a given channel
#if privmsg from different nick, same ident@host as an open privmsg window, show in that window and do updates?
#need x buttons for windows
#dividers in tab_widget like in mIRC?
#fix "your host is, \n running version ..." <- seems there's no bug, it was a server glitch.
#once it joined channels and didn't populate the nicks lists at all.  mIRC never did that.
#start text on bottom of window like mIRC
#show connection lost in channels and messagewindows
#detect bad username error if possible - can anything be done about it?  
#try to find out network name from server messages when we connect? is there a standard way?
#select and copy doesn't seem to work right. must be a qt bug.
#ability to add a hook on an arbitrary event (including a timer event) during run-time from input.  options to do it once or every time, only in a certain channel or network, etc.
#have nicks, username, realname, ident able to be defined in config file outside of specific networks
#ability to act as a bouncer or a client for it
#fix updating of ident and host so that it doesn't look through the whole nick list of each channel each time
#make nick_lower function
#have a global user list for each network and point to those users from the channels instead of having an independent list of users for each channel?

import os, sys, time, re, itertools, traceback
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import json
import qt4reactor_

if __name__ == "__main__": qt4reactor_.install()

#from twistedclient import SocketClientFactory
#from twisted.words.protocols import irc
import irc
from twisted.internet import protocol

def runidentd():
  identf = protocol.ServerFactory()
  identf.protocol = identd
  try:
    reactor.listenTCP(113,identf)
  except:
    print "Could not run identd server."
    #todo: show it in the gui 
  return identf

#if multiple lines inputted, detect if each line starts with "/" and run the command if it does?
class ServerInputQTextEdit(QTextEdit):
  def __init__(self, network):
    QTextEdit.__init__(self)
    self.network = network
    self.setAcceptRichText(False)
  def keyPressEvent(self, event):
    if event.key() == Qt.Key_Return:
      text = str(self.toPlainText())
      self.setPlainText("")
      if text.lstrip().startswith("/"):
        docommand("serverwindow", self.network.serverwindow, text)
      else:
        self.network.serverwindow.addline("* Nothing performed. This is not a channel or private-message window")
    else:
      QTextEdit.keyPressEvent(self, event)
      
      
class ChannelInputQTextEdit(QTextEdit):
  def __init__(self, channel):
    QTextEdit.__init__(self)
    self.channel = channel
    self.setAcceptRichText(False)

  def keyPressEvent(self, event):
    if event.key() == Qt.Key_Return and not (event.modifiers() and Qt.ShiftModifier):
      text = str(self.toPlainText())
      self.setPlainText("")
      if text.lstrip().startswith("/"):
        docommand("channelwindow", self.channel.channelwindow, text)
      else:
        if self.channel.network.server.serverconnection:
          self.channel.network.server.serverconnection.msg(self.channel.name, text)
          for msg in text.split(r"\n"):
            self.channel.channelwindow.addline("<%s> %s" % (self.channel.network.server.serverconnection.nickname, msg))
        else:
          self.channel.channelwindow.addline("* You are not currently connected to a server")
    else:
      QTextEdit.keyPressEvent(self, event)
      
def docommand(windowtype, window, text): #todo: test from server, channel, and privmsg
  params = text.split()   
  if params[0].lower() == "/join":
    if len(params) in (2, 3):
      if window.network.server.serverconnection:
        window.network.server.serverconnection.join(*params[1:])
      else:
        window.addline("* You are not currently connected to a server")
    else:
      window.addline("* Usage: /join <channel> [key]")
  else:
    window.addline("* Command not recognized")

class MessageInputQTextEdit(QTextEdit):
  def __init__(self, messagewindow):
    QTextEdit.__init__(self)
    self.messagewindow = messagewindow
    self.setAcceptRichText(False)

  def keyPressEvent(self, event):
    if event.key() == Qt.Key_Return and not (event.modifiers() and Qt.ShiftModifier):
      text = str(self.toPlainText())
      self.setPlainText("")
      if text.lstrip().startswith("/"):
        docommand("serverwindow", messagewindow, text)
      else:
        if self.messagewindow.network.server.serverconnection:
          self.messagewindow.network.server.serverconnection.msg(self.nick, text)
          for msg in text.split(r"\n"):
            self.messagewindow.addline("<%s> %s" % (self.messagewindow.network.server.serverconnection.nickname, msg))
        else:
          self.messagewindow.addline("* You are not currently connected to a server")
    else:
      QTextEdit.keyPressEvent(self, event)


class MessageWindow(QWidget):
  def __init__(self, network, nick):
    QWidget.__init__(self)
    self.network = network
    tab_widget.addTab(self, nick)
    self.textwindow = QTextEdit(self)
    self.textwindow.setReadOnly(True)
    self.textwindow.setFont(font)
    self.textWindow.setStyleSheet("* {position: absolute; bottom: 0}")
    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.addWidget(self.textwindow)
    self.editwindow = MessageInputQTextEdit(network) #self, network
    self.editwindow.setFont(font)
    self.layout.addWidget(self.editwindow)
    #sizepolicy = QSizePolicy()
    #sizepolicy.setVerticalPolicy()
    #self.editwindow.setSizePolicy(sizepolicy)
    self.editwindow.setFixedHeight(40) #todo: find out the pixel height of two lines of the font in its current size and use that. do this for all editwindows.
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
    self.textwindow.moveCursor(QTextCursor.End) #not sure this is necessary, it was in an example for doing this for some reason. (something about Qt adding extra newlines)
    scrollbar = self.textwindow.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())

#class ChannelNicks(QTextEdit):
#  def __init__(self):
#    QTextEdit.__init__(self)
    
class IRCClient(irc.IRCClient):
  
  def __init__(self):
    self.signedon = False
    self.nickindex = 0

  def connectionMade(self):
    irc.IRCClient.connectionMade(self)
    self.factory.conn = self
    
  def signedOn(self):
    #print "signed on"
    self.server.network.serverwindow.addline("* You are now signed on.")
    self.signedon = True
    tab_widget.setTabText(tab_widget.indexOf(self.server.network.serverwindow), "%s - %s" % (self.server.network.config["name"], self.nickname))
    
  def IRCcommand(self, command, prefix, params): #relies on a change to irc.py
    #print [command, prefix, params]
    self.server.network.serverwindow.addline(repr([command, prefix, params])) #debug 
    #if command not in ("PING", "PONG", "MODE", "RPL_NAMREPLY", "RPL_ENDOFNAMES", "JOIN", "RPL_TOPIC", "333"): #todo: handle notice and add it to this list. and of course, only show params
    self.server.network.serverwindow.addline(' '.join(params[1:]))
      
  def nickChanged(self, newnick):
    self.nickname = newnick
    self.server.network.serverwindow.addline("* Your nick has been changed to " + newnick)
    tab_widget.setTabText(tab_widget.indexOf(self.server.network.serverwindow), "%s - %s" % (self.server.network.config["name"], self.nickname))
    for channel in self.server.network.channels.values():
      channel.channelwindow.addline("* Your nick has been changed to " + newnick)
    for messagewindow in self.server.network.messagewindows:
      messagewindow.addline("* Your nick has been changed to " + newnick)
      
  def kickedFrom(self, channelname, kicker, message):
    channels = self.server.network.channels
    channel = channels[channelname.lower()]
    nick, ident, host = splithostname(kicker)
    channel.channelwindow.addline("* You were kicked from %s by %s (%s@%s) for reason: %s" % (channelname, nick, ident, host, message))
    for user in [user for user in channel.users.values() for channel in channels.values() if user.nick==nick]:
      if ident: user.ident = ident
      if host: user.host = host
    nickslist = channel.nickslist
    for (nick_lower, user) in channel.users.iteritems():
      nickslist.takeItem(nickslist.row(user.item))
      del channel.users[nick_lower]
 
  def userKicked(self, kickednick, channelname, kicker, message):
    kickernick, kickerident, kickerhost = splithostmask(kicker)
    kickednick_lower = kickednick.lower()
    for user in [user for user in channel.users.values() for channel in channels.values() if user.nick==kickernick]:
      if kickerident: user.ident = kickerident
      if kickerhost: user.host = kickerhost
    channel = self.server.network.channels[channelname.lower()]
    channel.channelwindow.addline("* %s was kicked from %s by %s (%s@%s) for reason: %s" % (kickednick, channelname, kickernick, kickerident, kickerhost, message))
    nickslist = channel.channelwindow.nickslist
    nickslist.takeItem(nickslist.row(channel.users[kickednick_lower].item))
    del channel.users[kickednick_lower]
 
  def userRenamed(self, oldnick, newnick):
    oldnick_lower = oldnick.lower()
    for channel in self.server.network.channels.values():
      if oldnick_lower() in channel.users:
        user = channel.users[oldnick_lower]
        channel.users[newnick.lower()] = user
        del channel.users[oldnick_lower]
        user.nick = newnick
        user.item.setText(user.prefix + newnick)
        channel.addline("* %s is now %s" % (oldnick, newnick))
    if oldnick_lower in self.server.network.messagewindows:
      messagewindows = self.server.network.messagewindows
      messagewindow = messagewindows[oldnick_lower]
      messagewindows[newnick.lower()] = messagewindow
      del messagewindows[oldnick_lower]
      tab_widget.setTabText(tab_widget.indexOf(self), newnick)
      messagewindow.addline("* %s is now %s" % (oldnick, newnick))
    
  def privmsg(self, fromhostmask, target, msg):
    target_lower = target.lower()
    nick, ident, host = splithostmask(fromhostmask)
    msg = QString.fromUtf8(msg)
    #msg = msg.decode("utf-8")
    if target_lower in self.server.network.channels:
      channel = self.server.network.channels[target_lower]
      nick, ident, host = splithostmask(fromhostmask)
      #channel.channelwindow.addline("<%s> %s" % (nick, msg))
      colorify(channel.channelwindow.textwindow, "<%s> %s" % (nick, msg))
      channel.channelwindow.addline("") 
      #if nick.lower() in channel.users: #I'm not including this line because if the result is false then there's a bug anyway
      user = channel.users[nick.lower()]
      user.nick = nick
      if ident: user.ident = ident
      if host: user.host = host
    elif target == self.nickname:
      fromnick_lower = nick.lower()
      if fromnick_lower not in self.server.network.messagewindows:
        self.server.network.messagewindows[fromnick_lower] = MessageWindow(self.server.network, nick)
        ding.play()
      messagewindow = self.server.network.messagewindows[fromnick_lower]
      messagewindow.addline("<%s> %s" % (nick, msg))
    else:
      print 'error: privmsg not to an open channel or to my nick. from: "%s"; to: "%s"; message: "%s"' % (fromhostmask, target, msg)
    
  def userJoined(self, hostmask, channelname): #relies on a change to irc.py
    nick, ident, host = splithostmask(hostmask)
    channels = self.server.network.channels
    channel = channels[channelname.lower()]
    channel.channelwindow.addline("* %s (%s@%s) has joined %s" % (nick, ident, host, channel.name))
    user = ChannelUser(nick)
    channel.users[nick.lower()] = user
    item = NickItem(nick, user)
    user.item = item
    for user in [user for user in channel.users.values() for channel in channels.values() if user.nick==nick]:
      if ident: user.ident = ident
      if host: user.host = host
 
  def userLeft(self, hostmask, channelname):
    nick, ident, host = splithostmask(hostmask)
    nick_lower = nick.lower()
    channel = self.server.network.channels[channelname.lower()]
    channel.channelwindow.addline("* %s (%s@%s) has left %s" % (nick, ident, host, channel.name))
    nickslist = channel.channelwindow.nickslist
    nickslist.takeItem(nickslist.row(channel.users[nick_lower].item))
    del channel.users[nick_lower]
 
  def userQuit(self, hostmask, quitmsg):
    nick, ident, host = splithostmask(hostmask)
    nick_lower = nick.lower()
    for channel in self.server.network.channels.values():
      if nick_lower in channel.users.keys(): #not sure it's safe to modify the dict while iterating over it but using .keys() should be fine
        channel.channelwindow.addline("* %s (%s@%s) has quit IRC: %s" % (nick, ident, host, quitmsg))
        nickslist = channel.channelwindow.nickslist
        nickslist.takeItem(nickslist.row(channel.users[nick_lower].item))
        del channel.users[nick_lower]
    messagewindow = self.server.network.messagewindows.get(nick_lower)
    if messagewindow:
      messagewindow.addline("* %s (%s@%s) has quit IRC: %s" % (nick, ident, host, quitmsg))
    
  def modeChanged(self, hostmask, channelname, added, removed): #problem: displaying mode changes the way i do may mislead users about how one *sets* modes.
    channel = self.server.network.channels.get(channelname.lower())
    nick, ident, host = splithostmask(hostmask)
    if channel is not None:
      nmd = {"q": "~", "a": "&", "o": "@", "h": "%", "v": "+"} #is this the way a *real* irc client updates nicks in the nick list upon mode change?
      mctexts = []
      for mc in added:
        if mc[1]:
          mctexts.append("+%s %s" % mc)
          nickprefix = nmd.get(mc[0])
          if nickprefix:
            user = channel.users.get(mc[1].lower())
            if user: #something is wrong if user is None, but i'm not just asssuming it won't be because then if it is the mode changes won't be shown in channel, and also it won't process the rest of the mode changes.
              user.prefix = nickprefix
              user.item.setText(nickprefix + mc[1])
        else:
          mctexts.append("+" + mc[0])
      for mc in removed:
        if mc[1]:
          mctexts.append("-%s %s" % mc)
          nickprefix = nmd.get(mc[0])
          if nickprefix:
            user = channel.users.get(mc[1].lower())
            if user: #something is wrong if user is None, but i'm not just asssuming it won't be because then if it is the mode changes won't be shown in channel, and also it won't process the rest of the mode changes.
              if user.prefix == nickprefix:
                user.prefix = ""
                user.item.setText(mc[1])
        else:
          mctexts.append("-" + mc[0])
      channel.channelwindow.addline("* %s sets mode(s): %s" % (nick, ", ".join(mctexts)))
      user = channel.users[nick.lower()]
      if ident: user.ident = ident
      if host: user.host = host
    else:
      if channelname == self.nickname:
        mctexts = []
        for mc in added:
          if mc[1]:
            mctexts.append("+%s %s" % mc)
          else:
            mctexts.append("+" + mc[0])
        for mc in removed:
          if mc[1]:
            mctexts.append("-%s %s" % mc)
          else:
            mctexts.append("-" + mc[0])
        self.server.network.serverwindow.addline("* %s sets mode(s): %s" % (nick, ", ".join(mctexts)))
      else:
        print "error: mode changes but target not recognized as a channel i'm in or as my own nick.  channelname: \"%s\"; self.nickname: \"%s\"" % (channelname, self.nickname)
  
  def joined(self, channelname):
    channelname_lower = channelname.lower()
    channel = Channel(channelname, self.server.network)
    channelwindow = ChannelWindow(channel, self.server.network)
    channel.channelwindow = channelwindow
    self.server.network.channels[channelname_lower] = channel
    app.processEvents()
    sizes = channelwindow.splitter.sizes()
    channelwindow.splitter.setSizes([sum(sizes)-150, 150])
  
  def irc_RPL_WELCOME(self, prefix, params):
    if params[1].startswith("Welcome to the "):
      networkname = params[1].split()[3] #do network names ever have more than one word in them? i'm only capturing one word because i saw both "irc network" and "internet chat relay network" after this word
      oldnetworkname = getattr(self, networkname, None) #should networkname go under network, server or serverconnection? 
      self.networkname = networkname
      if oldnetworkname and (networkname.lower() != oldnetworkname.lower()): #calling .lower is the Right Thing to do, right? 
        self.changednetworks(oldnetworkname, networkname)
        #todo: we may also want to do something if networkname.lower() != self.server.network.config["name"].lower()
        
  def changednetworks(oldnetworkname, newnetworkname):
    pass #todo: eventually we should probably make this warn the user and/or close or clear all channel and message windows for this network instance, once i'm comfortable that there are few to no false positives.
      
  def irc_RPL_NAMREPLY(self, prefix, params):
    channelname_lower = params[2].lower()
    for nick in params[3].split():
      nmo = re.match(r"([^a-zA-Z_[\]{}^`|]*).*", nick) #numbers and - can't be first character of a nick
      np = nick[:nmo.end(1)]
      nwp = nick[nmo.end(1):]
      nwp_lower = nwp.lower()
      user = ChannelUser(nwp, prefix=np)
      channel = self.server.network.channels[channelname_lower]
      channel.users[nwp_lower] = user
      #self.server.channels[channelname_lower].channelwindow.nickslist.insertHtml(nick + "<br>")
      item = NickItem(nick, user)
      channel.channelwindow.nickslist.addItem(item)
      channel.users[nwp_lower].item = item
      
  def irc_ERR_NICKNAMEINUSE(self, prefix, params):
    if not self.signedon: #should test if this is correct.
      oldnick = self.server.network.config["nicks"][self.nickindex]
      self.nickindex = (self.nickindex+1) % len(self.server.network.config["nicks"])
      newnick = self.server.network.config["nicks"][self.nickindex].encode("ascii")
      self.server.network.serverwindow.addline('* Nick "%s" is taken. Changing nick to "%s"' % (oldnick, newnick))
      self.setNick(newnick)
      self.nickname = newnick #do i have to do this?
    else:
      self.server.network.serverwindow.addline(' * Nick "%s" already in use' % XXX)#todo: find out where %s is in the params
      
  def irc_ERR_ERRONEUSNICKNAME(self, prefix, params):
    if not self.signedon: #should test if this is correct.
      oldnick = self.server.network.config["nicks"][self.nickindex]
      self.nickindex = (self.nickindex+1) % len(self.server.network.config["nicks"])
      newnick = self.server.network.config["nicks"][self.nickindex].encode("ascii")
      self.server.network.serverwindow.addline('* Nick "%s" is taken. Changing nick to "%s"' % (oldnick, newnick)) #todo: use oldnick from params instead of config.
      self.setNick(newnick)
      self.nickname = newnick #do i have to do this?
    else:
      self.server.network.serverwindow.addline(' * "%s" is an invalid nick' % XXX)#todo: find out where %s is in the params
      
  def startedConnecting(self, connector):
        pass
  
  def clientConnectionLost(self, connector, reason):
      """If we get disconnected, reconnect to server."""
      self.serverconnection = None
      self.network.serverwindow.addline("* Disconnected. Reconnecting...")
      #reactor.callLater(reconnectdelay, connector.connect)
      for channel in self.network.channels.values():
        channel.channelwindow.nickslist.clear()
      #self.network.channels = {} #todo: maybe we shouldn't do this because the windows are still open. just empty the users.
      protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

      #connector.connect()
      
class Client(protocol.ClientFactory):
  protocol = IRCClient
  def __init__(self, networkname, servers, mynicks, password, username, realname):
    self.nickindex = 0
    self.serverindex = 0
    self.protocol.nickname = mynicks[self.nickindex]
    self.serverslist = servers
    self.networkname = networkname
    self.mynicks = mynicks
    self.username = username
    self.realname = realname
  
  def clientConnectionFailed(self, connector, reason):
    self.serverconnection = None
    oldaddr, oldport = self.serverslist[self.network.serverindex]
    addr, port = self.serverslist[self.network.serverindex]
    self.network.serverwindow.addline("* Connection to (%s, %d) failed. Connecting to (%s, %d)..." % (oldaddr, oldport, addr, port)) #todo: add reason for fail
    self.network.serverindex = (self.network.serverindex+1) % len(self.network.config["servers"])
    #reactor.callLater(reconnectdelay, reactor.connectTCP, addr.encode("ascii"), port, self)
    #reactor.connectTCP(addr, port, self) #is this feasible? i don't know a better way to do this. connector.connect() apparently doesn't take server/port as arguments.
    
    for script in activescripts:
      obj = getattr(script.script, name, None)
      try:
        if obj and obj(self, connector.factory, reason): #connector.factory works?
          break
      except:
        traceback.print_exc()
    
    protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
      
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
    self.textwindow.setFont(font)
    self.textwindow.setStyleSheet("* {position: absolute; bottom: 0}") #doesn't work
    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.addWidget(self.textwindow)
    self.editwindow = ServerInputQTextEdit(network) #self, network
    self.editwindow.setFont(font)
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
    self.textwindow.moveCursor(QTextCursor.End) #not sure this is necessary, it was in an example for doing this for some reason.
    scrollbar = self.textwindow.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())
      
class Channel:
  def __init__(self, channelname, network):
    self.name = channelname
    self.users = {}
    self.network = network
  #def adduser(nick, prefix=None, hostmask=None):
  #  self.users[nick] = ChannelUser(nick, prefix, hostmask)
  #  self.channelwindow.nickslist.setHtml("<br>".join(sorted(self.users.keys()))) #fortunately nicks can't have < or > in them. if i weren't lazy i would replace them anyway with &lt or whatever (assuming pyqt even supports that)
    
class ChannelUser:
  def __init__(self, nick, prefix=None, ident=None, host=None):
    self.prefix = prefix
    self.host = host
    self.nick = nick
    self.ident = ident
      
class ChannelWindow(QWidget):
  def __init__(self, channel, network):
    QWidget.__init__(self)
    self.tab_index = tab_widget.addTab(self, channel.name)
    tab_widget.setCurrentIndex(self.tab_index)
    self.splitter = QSplitter(self)
    self.nickslist = QListWidget(self)
    self.nickslist.setSortingEnabled(True)
    self.nickslist.setFont(font)
    #self.nickslist.setReadOnly(True) #in case we change this back to a QTextEdit
    self.textwindow = QTextEdit(self)
    self.textwindow.setReadOnly(True)
    self.textwindow.setFont(font)
    self.textwindow.setStyleSheet("* {position: absolute; bottom: 0}")
    self.splitter.addWidget(self.textwindow)
    self.splitter.addWidget(self.nickslist)
    self.network = network
    self.vlayout = QVBoxLayout(self)
    self.vlayout.setContentsMargins(0, 0, 0, 0)
    self.vlayout.addWidget(self.splitter)
    self.editwindow = ChannelInputQTextEdit(channel)
    self.editwindow.setFont(font)
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
    self.textwindow.moveCursor(QTextCursor.End) #not sure this is necessary, it was in an example for doing this for some reason.
    self.textwindow.insertHtml("<br>")
    scrollbar = self.textwindow.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())

class NickItem(QListWidgetItem):
  def __init__(self, nick, user):
    QListWidgetItem.__init__(self, nick)
    self.user = user
  def __lt__(self, other):
    return self.text().toLower() < other.text().toLower() #todo: is @ < +? 
  
class Network:
  def __init__(self, client, config):
    self.client = client
    self.config = config
    self.channels = {}
    self.messagewindows = {} #should this be another class whose objects have messagewindow as an attribute? and if so, what would i call the class?
    
def splithostmask(hostmask):
  if "!" in hostmask:
    nick, rest = hostmask.split("!", 1)
  else:
    nick, rest = hostmask, ""
  if "@" in rest:
    ident, host = rest.split("@", 1)
  else:
    ident, host = "", ""
  return nick, ident, host

colorre = re.compile("(?:\x03(?:\\d\\d?(?:,\\d\\d?)?)?)|\x02|\x1f|\x16|\x1d")
#irccolors = ["#FFFFFF",    "#000000", "#00007F",   "#009300",    "#FF0000",   "#7F0000",  "#9C009C",      "#FC7F00",
#              "#FFFF00",    "#00FC00",   "#009393",   "#00FFFF",     "#0000FC", "#FF00FF",     "#7F7F7F",      "#D2D2D2"]
irccolors = ((255,255,255), (0, 0, 0), (0, 0, 127), (0, 147, 00), (255, 0, 0), (127, 0, 0), (156, 0, 156), (252, 127, 0),
             (255,255,0), (0, 252, 0), (0, 147, 147), (0, 255, 255), (0, 0, 252), (255, 0, 255), (127, 127, 127), (210, 210, 210))
#irccolors = ["White", "Black", "Navy Blue", "Green", "Red", "Brown", "Purple", "Olive", "Yellow", "Lime Green", "Teal", "Aqua Light", "Royal Blue", "Hot Pink", "Dark Gray", "Light Gray"]
# actual names of colors from http://www.ircbeginner.com/ircinfo/colors.html - untested

def colorify(widget, msg): #should behave just like mIRC.
  matches = re.findall(colorre, msg)
  texts = re.split(colorre, msg)
  bold = False
  underline = False
  italics = False
  reversed = False
  origcolorf = widget.textColor()
  #origcolorb = widget.textBackgroundColor() #doesn't fucking work
  origcolorb = QColor(255, 255, 255) #todo: get this value from configuration, if we add a configuration option for this.  also, report a bug re textBackgroundColor. i think qt4 support is discontinuing december 2015.
  curcolorf = origcolorf
  curcolorb = origcolorb
  for (text, code) in itertools.izip_longest(texts, matches): 
    widget.insertPlainText(text)
    if code:
      if code == "\x02":
        bold = not bold
        widget.setFontWeight(QFont.Bold if bold else QFont.Normal) 
      elif code == "\x1f":
        underline = not underline
        widget.setFontUnderline(underline)
      elif code == "\x1d":
        italics = not italics
        widget.setFontItalic(italics)
      elif code == "\x16":
        reversed = not reversed
        if reversed:
          widget.setTextColor(origcolorb)
          widget.setTextBackgroundColor(origcolorf)
        else:
          widget.setTextColor(curcolorf)
          widget.setTextBackgroundColor(curcolorb)
      elif code[0] == "\x03":
        if code == "\x03":
          curcolorf = origcolorf
          curcolorb = origcolorb
          if not reversed:
            widget.setTextColor(curcolorf)
            widget.setTextBackgroundColor(curcolorb)
        else:
          codes = code[1:].split(",")
          curcolorf = QColor(*irccolors[int(codes[0])])
          widget.setTextColor(curcolorf)
          if len(codes) == 2:
            curcolorb = QColor(*irccolors[int(codes[1])])
            widget.setTextBackgroundColor(curcolorb)
  widget.setTextColor(origcolorf)
  widget.setTextBackgroundColor(origcolorb)

class identd(protocol.Protocol):
  def dataReceived(self, data):
    self.transport.write(data.strip() + " : USERID : UNIX : " + config.identid + "\r\n" )
    #todo: configure id per network
      
config = json.load(open("qttmwirc.conf.json"))
reconnectdelay = 3

from twisted.internet import reactor

class Script: 
  def __init__(self, module, script):
    self.module = module
    self.script = script

def loadscripts(networks):
  scripts = {}
  scriptspath = os.path.join(mypath, "scripts")
  for scriptfn in os.listdir(os.path.join(mypath, "scripts")):
    if not scriptfn.startswith("_"):
      scriptpath = os.path.join(scriptspath, scriptfn)
      if scriptfn.lower().endswith(".py"):
        scriptname = scriptfn[:-3]
      elif os.path.isdir(scriptpath):
        if os.path.exists(os.path.join(scriptpath, "__init__.py")):
          scriptname = scriptfn
      try:
        __import__("scripts."+scriptname)
        script = sys.modules["scripts."+scriptname]
        scripts[scriptname] = Script(script, script.Script(networks))
      except Exception, inst:
        raise #debug
        print 'Could not load script "%s" from "%s" because of error: %s' % (scriptname, scriptpath, inst.message)
        #todo: gui
  return scripts

def makefunc(name, obj):#one way to do closure in Python
  def f(self, *args, **kwargs): 
    for script in activescripts.itervalues():
      obj2 = getattr(script.script, name, None)
      try:
        if obj2 and obj2(self, *args, **kwargs):
          break
      except:
        traceback.print_exc()
    else:
      return obj(self, *args, **kwargs)
  return f
  
if __name__=="__main__":
  mypath = os.path.dirname(__file__)

  for name in dir(IRCClient):
    if not name.startswith('_'):
      obj = getattr(IRCClient, name)
      if callable(obj):
        setattr(IRCClient, name, makefunc(name, obj))
  
  app = QApplication([])
  
  networks = []
   
  font = QFont("Fixedsys Excelsior 3.01 NoLiga")
  #font = QFont("Arial")
  #font = QFont("Fixedsys") 
  #font.setPointSize(7) #fixedsys
  font.setPointSize(10) #fixedsys excelsior
  ding = QSound(r"sounds\01_ECHOBEL3.wav") #todo: find out how to get directory of this running python file and os.join that with sounds\whatever
  
  mainwindow = MainWindow()
  mainwindow.showMaximized()
  
  tab_widget = QTabWidget()
  vbox = QVBoxLayout() 
  vbox.addWidget(tab_widget)
  vbox.setContentsMargins(0, 0, 0, 0)
  mainwindow.setLayout(vbox)    
  
  for network_config in config["networks"]:
    networkname = network_config.get("name")
    mynicks = network_config.get("nicks")
    username = network_config.get("username")
    servers = network_config.get("servers")
    if username:
      username = username.encode("ascii")
    password = network_config.get("password")
    if password:
      password = password.encode("ascii")
    realname = network_config.get("realname")
    if realname:
      realname = realname.encode("ascii")
    network = Network(Client(networkname, servers, mynicks, password, username, realname), network_config)
    serverwindow = ServerWindow(network)
    #server.network = network
    network.serverwindow = serverwindow
    network.serverindex = 0
    networks.append(network)
    #reactor.connectTCP(network_config["servers"][0][0].encode("ascii"), network_config["servers"][0][1], server) 
  
  scripts = loadscripts(networks)
  activescripts = dict(scripts) #scripts currently running = a copy of all loaded script references
  identf = runidentd() 
  
  reactor.run()
  