
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ServerInputQTextEdit(QTextEdit):
  def __init__(self):
    QTextEdit.__init__(self)
  def keyPressEvent(self, event):
    print "sizes from keypress:", channelwindow.splitter.sizes()
    
class MainWindow(QWidget): 
    def __init__(self): 
        QWidget.__init__(self) 
        self.setWindowTitle("qttmwirc")         
    def closeEvent(self, event):
      pass
      
class ChannelWindow(QWidget):
  def __init__(self, channel):
    QWidget.__init__(self)
    self.tab_index = tab_widget.addTab(self, channel)
    tab_widget.setCurrentIndex(self.tab_index)
    self.splitter = QSplitter(self)
    self.nickslist = QTextEdit(self)
    self.nickslist.setReadOnly(True)
    self.textwindow = QTextEdit(self)
    self.textwindow.setReadOnly(True)
    self.splitter.addWidget(self.textwindow)
    self.splitter.addWidget(self.nickslist)
    self.vlayout = QVBoxLayout(self)
    self.vlayout.setContentsMargins(0, 0, 0, 0)
    self.vlayout.addWidget(self.splitter)
    self.editwindow = ServerInputQTextEdit()
    self.vlayout.addWidget(self.editwindow)
    nickswidth = self.nickslist.width()
    textwidth = self.textwindow.width()
    self.nickslist.setMinimumSize(0,0)
    width = self.width()
    print "self.width before setsizes:", width
    print "nicks & text widths before setsizes:", nickswidth, textwidth
    print "splitter width before setsizes:",self.splitter.width()
    print "splitter.geometry.width before setsizes:", self.splitter.geometry().width()
    self.splitter.setSizes([width-50, 50]) 
    self.splitter.setStretchFactor(self.splitter.indexOf(self.nickslist), 0)
    nickswidth = self.nickslist.width()
    textwidth = self.textwindow.width()
    width = self.width()
    print "self.width after setsizes:", width
    print "nicks & text widths after setsizes:", nickswidth, textwidth
    print "splitter width after setsizes:",self.splitter.width()
    print "splitter.geometry.width after setsizes:", self.splitter.geometry().width()
    self.editwindow.setFixedHeight(40)
    print "sizes from channelwindow:", self.splitter.sizes()
from twisted.internet import reactor

app = QApplication([])
    
mainwindow = MainWindow()
mainwindow.showMaximized()

tab_widget = QTabWidget()
vbox = QVBoxLayout()  
vbox.addWidget(tab_widget)
vbox.setContentsMargins(0, 0, 0, 0)
mainwindow.setLayout(vbox)      
app.processEvents()
channelwindow = ChannelWindow("test")
app.processEvents()
print "sizes from main:", channelwindow.splitter.sizes()

sys.exit(app.exec_())
