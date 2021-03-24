class test():
  def __getitem__(self, item):
    print item

t = test()
t[1]
for x in t:
  pass
