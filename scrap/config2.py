class Config(object):
  def __init__(self, value):
    self.value = value
  def __getitem__(self, index):
    return Config(self.value[index])
  def __getattr__(self, attr):
    return Config(self.value[attr])
  def __getslice__(self, start, end):
    return [Config(item) for item in self.value]

config = Config(json.load(open("qttmwirc.conf.json")))
print config.networks

