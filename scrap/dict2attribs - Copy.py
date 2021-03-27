def json_dict_to_namespaces(b):
  if type(b) == list:
    o = []
    for e in b:
      o.append(json_dict_to_namespaces(e))
  elif type(b) == dict:
    class O(object):
      def __init__(self, d):
        self.d = d
      def __getattr__(self, attr):
        if attr in self.d:
          return json_dict_to_namespaces(self.d[attr])
        else:
          return None
    o = O(b)
  #elif type(b) in (unicode, int, float):
  else:
    o = b
  return o

import json
config = json.load(open("qttmwirc.conf.json"))
attrconfig = json_dict_to_namespaces(config)
print attrconfig.networks
print attrconfig.networks[0] 
print attrconfig.networks[0].username
print attrconfig.nicks[0]
print attrconfig.test
