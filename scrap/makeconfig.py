import json
open("qttmwirc.conf.json","w").write(json.dumps({"networks":
                   [
                     {
                       "name": "UnderNet",
                       "servers":
                        [
                          ("irc.undernet.org", 6667)
                        ],
                       "nicks": ["inhahe_", "inhahe`", "inhahe``"], #if identd doesn't work, you'll get a bad username error if you end or begin your nick with a _ or have more than one - or _
                       "username": "inhahe",
                       "channels": ["#scifi", "#psychic"]
                     }     
                   ]
                 }))


