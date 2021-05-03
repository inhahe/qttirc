from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


irccolors = ((255,255,255), (0, 0, 0), (0, 0, 127), (0, 147, 00), (255, 0, 0), (127, 0, 0), (156, 0, 156), (252, 127, 0),
             (255,255,0), (0, 252, 0), (0, 147, 147), (0, 255, 255), (0, 0, 252), (255, 0, 255), (127, 127, 127), (210, 210, 210),
             (71,0,0), (71, 33, 0), (71, 71, 0), (50, 71, 0), (0, 71, 0), (0, 71, 44), (0, 71, 71), (0, 39, 71), (0, 0, 71), (46, 0, 71), (71, 0, 71), (71, 0, 42),
             (116, 0, 0), (116, 58, 0), (116, 116, 0), (81, 116, 0), (0, 116, 0), (0, 116, 73), (0, 116, 116), (0, 64, 116), (0, 0, 116), (75, 0, 116), (116, 0, 116), (116, 0, 69),
             (181, 0, 0), (181, 99, 0), (181, 181, 0), (125, 181, 0), (0, 181, 0), (0, 181, 113), (0, 181, 181), (0, 99, 181), (0, 0, 181), (117, 0, 181), (181, 0, 181), (181, 0, 107),
             (255, 0, 0), (255, 140, 0), (255, 255, 0), (178, 255, 0), (0, 255, 0), (0, 255, 160), (0, 255, 255), (0, 140, 255), (0, 0, 255), (165, 0, 255), (255, 0, 255), (255, 0, 152),
             (255, 89, 89), (255, 180, 89), (255, 255, 113), (207, 255, 96), (111, 255, 111), (111, 255, 201), (109, 255, 255), (89, 180, 255), (89, 89, 255), (196, 89, 255), (255, 102, 255), (255, 89, 188),
             (255, 156, 156), (255, 211, 156), (255, 255, 156), (226, 255, 156), (156, 255, 156), (156, 255, 219), (156, 255, 255), (156, 211, 255), (156, 156, 255), (220, 156, 255), (255, 156, 255), (255, 148, 211),
             (0, 0, 0), (19, 19, 19), (40, 40, 40), (54, 54, 54), (77, 77, 77), (101, 101, 101), (129, 129, 129), (159, 159, 159), (188, 188, 188), (226, 226, 226), (255, 255, 255))      


app = QApplication(sys.argv)

def colordistance(rgb1, rgb2):
  R1, G1, B1 = rgb1
  R2, G2, B2 = rgb2
  rbar = (R1+R2)/2
  return ((2+rbar/256) * (R2-R1)**2 + 4 + (G2-G1)**2 + (2+(255-rbar)/256)*(B2-B1)**2)**.5

def perceivedbrightness(r, g, b):
  r = r/255
  g = g/255
  b = b/255
  def vlinear(v):
    if v <= .04045:
      return v/12.92
    else:
      return ((v+.055)/1.055) ** 2.4
  def luminance(r, g, b):
    return vlinear(r*.2126) + vlinear(g)*.7152 + vlinear(b)*.0722
  y = luminance(r, g, b)
  if y <= 216/24389:    #   The CIE standard states 0.008856, but 216/24389 is the intent for 0.008856451679036
    return y * 24389/27 #   The CIE standard states 903.3, but 24389/27 is the intent, making 903.296296296296296
  else:
    return y**(1/3) * 116 - 16;
 
colorwidget = QWidget()
colorgrid = QGridLayout()
#colorgrid.setContentsMargins(0,0,0,0)
colorlabels = {}
# class ColorLabel(QLabel):
#   def __init__(self, fgcolor, bgcolor):
#     QLabel.__init__(self)
#     #self.setFixedWidth(self.height())
#     self.setFixedWidth(QFontMetrics(self.font()).height())
#     self.fgcolor = fgcolor
#     self.bgcolor = bgcolor
 #  def paintEvent(self, event):
 #    painter = QPainter()
 #    painter.begin(self)
 #    painter.fillRect(event.rect(), self.fgcolor)
 #    painter.end()
 #        
i = 0
for y in range(2):
  for x in range(8):
    colorlabel = QLabel()
    colorlabel.setFixedWidth(QFontMetrics(colorlabel.font()).height())
    #ColorLabel(QColor(*irccolors[y*8+x]), QColor(0, 0, 0))
    colorlabel.setAutoFillBackground(True)
    colorlabel.setAlignment(Qt.AlignCenter)
    #pal = colorlabel.palette()
    #pal.setColor(QPalette.Window, QColor(*irccolors[y*8+x]))
    #colorlabel.setPalette(pal)
    bgcolor = irccolors[i]
    #fgcolor = "white" if sum(bgcolor) < 384 else "black"
    fgcolor = "black" if perceivedbrightness(*bgcolor) >= 50 else "white"
    colorlabel.setStyleSheet(f"QLabel {{ background-color : rgb{bgcolor}; color : {fgcolor} }}")
    colorlabel.setText(str(i))
    colorlabels[x, y] = colorlabel
    colorgrid.addWidget(colorlabel, y, x, 1, 1)
    i += 1
    
for y in range(7):
  for x in range(12):
    if i < 99:
      colorlabel = QLabel()
      colorlabel.setFixedWidth(QFontMetrics(colorlabel.font()).height())
      #ColorLabel(QColor(*irccolors[y*8+x]), QColor(0, 0, 0))
      colorlabel.setAutoFillBackground(True)
      colorlabel.setAlignment(Qt.AlignCenter)
      #pal = colorlabel.palette()
      #pal.setColor(QPalette.Window, QColor(*irccolors[y*8+x]))
      #colorlabel.setPalette(pal)
      bgcolor = irccolors[i]
      #fgcolor = "white" if sum(bgcolor) < 384 else "black" #todo: do this better. maybe use a color distance algorithm to measure the distances to white and black?
      fgcolor = "black" if perceivedbrightness(*bgcolor) >= 50 else "white"
      colorlabel.setStyleSheet(f"QLabel {{ background-color : rgb{bgcolor}; color : {fgcolor} }}")
      colorlabel.setText(str(i))
      #colorlabels[x, y] = colorlabel
      colorgrid.addWidget(colorlabel, y+2, x, 1, 1)    
    i += 1 
colorwidget.setLayout(colorgrid)
colorwidget.show()

app.exec()