"Trivia Bot"

from __future__ import division
import qttmwirc
import irc
import cPickle, threading, random, os, re
import dameraulevenshtein, metaphone
from PyQt4.QtCore import QTimer, SIGNAL, SLOT

#should we provide channel objects or parent class for scripts to use?
#class Channel(ScriptChannel):
#  def __init__(self, channelname):
#    ScriptChannel.__init__(self, channelname)
##we should now have self.post, self.nicks, etc.
##should we have self.received()?
##should we have that in the main program?
##should channel methods pass main? 
##should they pass the Script instance?
##should they inherit Script? <i don't think so

#we need to be able to tell the irc network to forgo a response to an event after we
#process it

#change it so that one instance is created for all networks and before any connects
#make script list a dict

start = False

class Channel:
  def __init__(self, network, channel, start=False, interval=120):
    self.on = start
    self.network = network
    self.channel = channel
    self.interval = interval
    self.timer = QTimer()
    self.timer.connect(self.timer, SIGNAL("timeout()"), self.doquestion)
    if self.on:
      self.timer.start(1000)#kind of a hack.  problem is network.channels doesnt have the channel yet

  def post(self, message):
    self.network.channels[self.network.server.serverconnection.irclower(self.channel)].post(message)
    #self.network.channels[self.network.server.serverconnection.irclower(self.channel)].channelwindow.addlinecolored("<%s> %s" % (self.network.mynick, message))
      
  def nobodygotit(self):
    self.post("Nobody got it!  The answer was \x0310" + self.answer + "\x03.")
    self.doquestion()
  def doquestion(self):
    self.category, self.topics = random.choice(trivia.items())
    self.topic, (self.desc, self.questions) = random.choice(self.topics.items())
    self.question, (self.answer, self.explanation) = random.choice(self.questions)
    self.hint = re.sub("[a-zA-Z0-9]", '*', self.answer)
    self.post("Category:\x039 " + self.category)
    self.post("Topic:\x0313 " + self.topic + (" - " + self.desc if self.desc else ""))
    self.post("\x0312" + self.question)
    if self.on:  
      self.timer.stop()
      self.timer.start(self.interval*1000)
      self.timer.disconnect(self.timer, SIGNAL("timeout()"), self.nobodygotit)
      self.timer.disconnect(self.timer, SIGNAL("timeout()"), self.doquestion)
      self.timer.connect(self.timer, SIGNAL("timeout()"), self.nobodygotit)

class Script:
  def __init__(self, networks, dochnames=None, start=start, interval=30):
    self.networks = networks
    self.dochnames = defaultdochnames[:] if dochnames is None else dochnames[:]
    self.channels = {}
    for network in networks:
      for chname in self.dochnames:
        try:
          chnamelow = network.client.factory.conn.irclower(chname)
        except AttributeError:
          chnamelow = irc.irclower(chname)
        if chnamelow in network.channels:
          self.channels[network, chnamelow] = Channel(network, network.channels[chnamelow],
                                                     start=start, interval=interval)
    # we should have a convenience function for this 
          
  def networkchanged(self, conn, network, oldnetwork): #because network has just been reset by qttwirc.
    pass                                  #no need to pass oldconn here, because 
                                          #conn has alredy been erased with a
                                          #lostConnection() by this time.
                                          #I guess we need this function in case qttwirc tries to reconnect to a different server thinking it's the same network and it's not. really though i think we should kill the network/conn/channels/etc. instances whenever we disconnect.
  def command(self, window, cmd, params):
    pass
  
  def joined(self, conn, chname):
    self.channels[conn, conn.irclower(chname)] = Channel(conn.server.network, chname, start)
    
  def msg(self, conn, dest, text, wtf=None): #honestly don't know what the fifth parameter (None) i'm being passed is from
    if (conn, conn.irclower(dest)) in self.channels:
      self.chanmsg(conn, conn.server.network.mynick, dest, text)
    
  def privmsg(self, conn, user, message):
    pass
    
  def chanmsg(self, conn, user, channelname, message):
    ch = self.channels[conn, conn.irclower(channelname)]
    if message.strip().lower() == "!next":
      ch.nobodygotit()
    elif message.strip().lower() == "!stop":
      ch.on = False
      ch.timer.stop()
    elif message.strip().lower() == "!start":
      ch.on = True
      ch.doquestion()
    elif message.strip().lower() == "!hint":
      stars = [i for i, c in enumerate(ch.hint) if c == "*"]
      n = min(3, len(stars)-3)
      if n >= 1:
        for i in random.sample(stars, n):
          ch.hint = ch.hint[:i] + ch.answer[i] + ch.hint[i+1:]
      ch.post("Hint!!!!! \x037" + ch.hint)
    elif ch.on:
      inp = ' '.join(message.strip().lower().split())
      ans = ' '.join(ch.answer.strip().lower().split())
      if inp == ans:
        ch.post("%s got the answer!  %s" % (irc.usersplit(user).group("nick"), ch.explanation))
        ch.doquestion()
      elif dameraulevenshtein.dameraulevenshtein(inp, ans) / len(ans) <= .2:
        ch.post(message + "?  \x033That's close!")
        print "levenshtein"
      elif metaphone.dm(inp) == metaphone.dm(ans):
        ch.post(message + "?  \x033That's close!")
        print "metaphone"
  
trivia = cPickle.load(open(os.path.join(os.path.dirname(__file__), 'trivia2.pkl')))
      
