import re
def parseconfig(fn):
  lineno = 1
  f = open(fn)
  output = []
  levels = {}
  lindent = 0
  level = 0
  llevel = 0
  output = []
  for line in f:
    lineno += 1
    if line.strip():
      nline = line.lstrip()
      indent = len(line)-len(nline)
      if indent > lindent:
        level += 1
        levels[indent] = level 
      elif indent < lindent:
        try:
          level = levels[indent]
        except KeyError:
          raise ValueError('Improper indentation in config file "%s" line %d: "%s"' % (fn, lineno, line.strip()))
        for i in levels.keys():
          if i > indent:
            del levels[i]
      if level > llevel:
        s = "{"*(level-llevel) + nline
      elif level < llevel:
        s = "}"*(llevel-level) + nline
      else:
        s = nline
      output.append(s)
      llevel = level
      lindent = indent
  outputs = ''.join(output)

  tokens = ('LVSTRING', 'RVSTRING', 'SQUOTE', 'DQUOTE')
  t_LVSTRING = r"[a-zA-Z.]+"
  t_RVSTRING = r"[^, :{}]*"
  SQUOTE = r'"([^"\n]|(\\"))*"'
  DQUOTE = r"'([^'\n]|(\\'))*'"

  def p_
  
  
    



parseconfig('test.py')