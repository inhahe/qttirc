class Script:
  def __init__(self, networks, serverwindows, docommand):
    
    print("did this 1") #debug
    self.networks = networks
    self.docommand = docommand
    self.docommand("serverwindow", serverwindows[-1], "/server localhost")
                                    
  def irc_RPL_WELCOME(self, conn, prefix, params):
    if params[1].startswith("Welcome to the "):
      networkname = params[1].split()[3] #do network names ever have more than one word in them? i'm only capturing one word because i saw both "irc network" and "internet chat relay network" after this word
      if networkname == "Exalumen":
        self.docommand("serverwindow", conn.server.network.serverwindow, "/join #test")
        self.docommand("serverwindow", conn.server.network.serverwindow, "/join #test2")
  
  def joined(self, conn, chname):
    #self.channels[conn, conn.irclower(chname)] = Channel(conn.server.network, chname, start)
    pass
    
  def msg(self, conn, dest, text, wtf=None): #honestly don't know what the fifth parameter (None) i'm being passed is from
    #if (conn, conn.irclower(dest)) in self.channels:
    #  self.chanmsg(conn, conn.server.network.mynick, dest, text)
    pass
    
  def privmsg(self, conn, user, message):
    pass
    
  def chanmsg(self, conn, user, channelname, message):
    pass
      
  def newconn(self, conn): #haven't implemented this yet. should be called when a new connection is made. or is this already covered by an existing function? ConnectionMade?
    pass
  
  