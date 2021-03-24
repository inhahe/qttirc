#def colorify(msg):
#  #todo: instead of using html, should we use setTextColor, setTextBackgroundColor, setFontItalic, setFontUnderline, setFontWeight?
#  
#  #\x15 = ^U = underline, \x12 = ^R = reverse, \x09 = ^I = italics, \x0f = ^O = normal text
#  matches = re.findall(colorre, msg)
#  texts = re.split(colorre, msg)
#  results = []
#  bold = False
#  underline = False
#  colored = False
#  italics = False
#  for (text, code) in itertools.izip_longest(text, matches):
#    results.append(text)
#    if code:
#      if code == "\x02":
#        bold = not bold
#        results.append("<b>" if bold else "</b>")
#      elif code == "\x15":
#        underline = not underline
#        results.append("<u>" if underline else "</u>")
#      elif code == "\x09":
#        italics = not italics
#        results.append("<i>" if italics else "</i>")
#      elif code == "\x12":
#        
#      elif code[0] == "\x02":
#        html = ""
#        if colored:
#          html = "</font>"
#        if code != "\x02":
#          codes = code[1:].split(",")
#          if len(codes) == 1:
#            html += '<span color:"%s">' % irccolors[int(codes[0])]
#          else:
#            html += '<span color:%s; background-color:%s>' % (irccolors[int(codes[0])], irccolors[int(codes[1])])
#          results.append(html)
#      
#        
#  if bold:
#    results.append("")
#    results.append("</b>")
    
