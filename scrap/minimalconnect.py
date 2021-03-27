from twisted.words.protocols import irc 
from twisted.internet import protocol  
from twisted.internet import reactor

class ServerConnection(irc.IRCClient):
  
  def __init__(self):
    self.signedon = False
    self.nickindex = 0
  
  def signedOn(self):
    print("signed on")
        
  def nickChanged(self, newnick):
    self.nickname = newnick
          
class Network(object):
  def __init__(self, servers, mynick=None):
    self.servers = servers
    self.mynick = mynick
    self.serverindex = 0
    
class ServerFactory(protocol.ReconnectingClientFactory):
  def __init__(self, nickname="qttwirc", password=None, username="qttwirc", realname=None, network=None):
    self.network = network
    self.network.mynick = nickname
    self.nickname = nickname
    self.username = username
    self.password = password
    self.realname = realname
    protocol.ReconnectingClientFactory.initialDelay = 10 #should i leave this at 1?
    protocol.ReconnectingClientFactory.maxDelay = 10 #no idea what value this should be. 3.5 wasn't slow enough, i was being throttled.
    
  def buildProtocol(self, addr):
    p = ServerConnection()
    self.serverconnection = p
    p.server = self
    p.nickname = self.nickname
    p.username = self.username
    self.resetDelay()
    return p

  def clientConnectionLost(self, connector, reason):
    self.serverconnection = None
    protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

  def clientConnectionFailed(self, connector, reason):
    self.serverconnection = None
    addr, port = self.network.servers[self.network.serverindex]
    self.network.serverindex = (self.network.serverindex+1) % len(self.network.servers) #todo: make it actually use these values
    
    #reactor.callLater(config.reconnectdelay, reactor.connectTCP, addr.encode("ascii"), port, self)
    #reactor.connectTCP(addr, port, self) #is this feasible? i don't know a better way to do this. connector.connect() apparently doesn't take server/port as arguments.
    
    protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
    
network = Network([("hitchcock.freenode.net", 6667), ("verne.freenode.net", 6667)])
server = ServerFactory(nickname="test123", username="test123", network=network)   
reactor.connectTCP(*network.servers[network.serverindex], server)
reactor.run()
