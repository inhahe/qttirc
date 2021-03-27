class O(object):
  def __init__(self, d):
    self.d = d
  def __getattr__(self, attr):
    if attr in self.d:
      return self.d[attr]
    else:
      return None
o = O({"test": "1234"})

print o.test
print o.blah