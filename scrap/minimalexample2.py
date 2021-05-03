from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    self.tab_widget = QTabWidget()
    self.vbox = QVBoxLayout() 
    self.vbox.addWidget(self.tab_widget)
    self.vbox.setContentsMargins(0, 0, 0, 0)
    self.setCentralWidget(self.tab_widget)
    self.showMaximized()

class ChannelWindow(QWidget):
  def __init__(self):
    QWidget.__init__(self)
    self.tab_index = mainwin.tab_widget.addTab(self, "channel window")
    mainwin.tab_widget.setCurrentIndex(self.tab_index)
    self.textwindow = QTextEdit(self)
    self.splitter = QSplitter(self)
    self.splitter.addWidget(self.textwindow)
    self.vlayout = QVBoxLayout(self)
    self.vlayout.setContentsMargins(0, 0, 0, 0)
    self.vlayout.addWidget(self.splitter)
    self.editwindow = ChannelInputQTextEdit()
    self.editwindow.setFocus()
    self.vlayout.addWidget(self.editwindow)
    self.editwindow.setFixedHeight(40)
    self.editwindow.setFocus()
    
class ChannelInputQTextEdit(QTextEdit):
  def keyPressEvent(self, event):
    if event.key() == 75 and (event.modifiers() & Qt.ControlModifier):
      widget = QDialog(channelwindow)
      label = QLabel()
      label.setText("Test")
      grid = QGridLayout()
      grid.addWidget(label, 1, 1, 1, 1)
      widget.setLayout(grid)
      widget.raise_()
      widget.show()
      size = widget.frameSize()
      w, h = size.width(), size.height()
      widget.move(max(self.mapToParent(self.cursorRect().topLeft()).x() - w/2, 0),  self.y() - h) 
      self.widget = widget
      self.setFocus()
      self.activateWindow()
    else:
      QTextEdit.keyPressEvent(self, event)

mainwin = MainWindow()
channelwindow = ChannelWindow()
app.exec()
