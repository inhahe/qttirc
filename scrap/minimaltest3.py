#!/usr/bin/python3
"""
Prototype of a window with twisted
"""

import sys
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
        QAction, QActionGroup, QApplication, QFrame, QLabel, QMainWindow,
        QMenu, QMessageBox, QSizePolicy, QVBoxLayout, QWidget)
HAS_QDARKSTYLE = False
try:
    import qdarkstyle
    HAS_QDARKSTYLE = True
except ImportError:
    pass


class MainWindow(QMainWindow):
    """
    Main window.
    """
    def __init__(self):
        super(MainWindow, self).__init__()

        _central_widget = QWidget()
        self.setCentralWidget(_central_widget)

        _top_filler = QWidget()
        _top_filler.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._info_label = QLabel(
                "<i>Choose a menu option, or right-click to invoke a context menu</i>",
                alignment=Qt.AlignCenter)
        self._info_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        _bottom_filler = QWidget()
        _bottom_filler.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        _vbox = QVBoxLayout()
        _vbox.setContentsMargins(5, 5, 5, 5)
        _vbox.addWidget(_top_filler)
        _vbox.addWidget(self._info_label)
        _vbox.addWidget(_bottom_filler)
        _central_widget.setLayout(_vbox)

        self.createActions()
        self.createMenus()

        _message = "A context menu is available by right-clicking"
        self.statusBar().showMessage(_message)

        self.setWindowTitle("Menus")
        self.setMinimumSize(360, 240)
        self.resize(720, 480)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.addAction(self.cutAct)
        menu.addAction(self.copyAct)
        menu.addAction(self.pasteAct)
        menu.exec_(event.globalPos())

    def newFile(self):
        self._info_label.setText("Invoked <b>File|New</b>")

    def open(self):
        self._info_label.setText("Invoked <b>File|Open</b>")

    def save(self):
        self._info_label.setText("Invoked <b>File|Save</b>")

    def print_(self):
        self._info_label.setText("Invoked <b>File|Print</b>")

    def undo(self):
        self._info_label.setText("Invoked <b>Edit|Undo</b>")

    def redo(self):
        self._info_label.setText("Invoked <b>Edit|Redo</b>")

    def cut(self):
        self._info_label.setText("Invoked <b>Edit|Cut</b>")

    def copy(self):
        self._info_label.setText("Invoked <b>Edit|Copy</b>")

    def paste(self):
        self._info_label.setText("Invoked <b>Edit|Paste</b>")

    def bold(self):
        self._info_label.setText("Invoked <b>Edit|Format|Bold</b>")

    def italic(self):
        self._info_label.setText("Invoked <b>Edit|Format|Italic</b>")

    def leftAlign(self):
        self._info_label.setText("Invoked <b>Edit|Format|Left Align</b>")

    def rightAlign(self):
        self._info_label.setText("Invoked <b>Edit|Format|Right Align</b>")

    def justify(self):
        self._info_label.setText("Invoked <b>Edit|Format|Justify</b>")

    def center(self):
        self._info_label.setText("Invoked <b>Edit|Format|Center</b>")

    def setLineSpacing(self):
        self._info_label.setText("Invoked <b>Edit|Format|Set Line Spacing</b>")

    def setParagraphSpacing(self):
        self._info_label.setText("Invoked <b>Edit|Format|Set Paragraph Spacing</b>")

    def about(self):
        self._info_label.setText("Invoked <b>Help|About</b>")
        QMessageBox.about(self, "About Menu",
                "The <b>Menu</b> example shows how to create menu-bar menus "
                "and context menus.")

    def aboutQt(self):
        self._info_label.setText("Invoked <b>Help|About Qt</b>")

    def createActions(self):
        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
            statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QAction("&Open...", self, shortcut=QKeySequence.Open,
            statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
            statusTip="Save the document to disk", triggered=self.save)

        self.printAct = QAction("&Print...", self, shortcut=QKeySequence.Print,
            statusTip="Print the document", triggered=self.print_)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
            statusTip="Exit the application", triggered=self.close)

        self.undoAct = QAction("&Undo", self, shortcut=QKeySequence.Undo,
            statusTip="Undo the last operation", triggered=self.undo)

        self.redoAct = QAction("&Redo", self, shortcut=QKeySequence.Redo,
            statusTip="Redo the last operation", triggered=self.redo)

        self.cutAct = QAction("Cu&t", self, shortcut=QKeySequence.Cut,
            statusTip="Cut the current selection's contents to the clipboard",
            triggered=self.cut)

        self.copyAct = QAction("&Copy", self, shortcut=QKeySequence.Copy,
            statusTip="Copy the current selection's contents to the clipboard",
            triggered=self.copy)

        self.pasteAct = QAction("&Paste", self, shortcut=QKeySequence.Paste,
            statusTip="Paste the clipboard's contents into the current selection",
            triggered=self.paste)

        self.boldAct = QAction("&Bold", self, checkable=True,
            shortcut="Ctrl+B", statusTip="Make the text bold",
            triggered=self.bold)

        boldFont = self.boldAct.font()
        boldFont.setBold(True)
        self.boldAct.setFont(boldFont)

        self.italicAct = QAction("&Italic", self, checkable=True,
            shortcut="Ctrl+I", statusTip="Make the text italic",
            triggered=self.italic)

        italicFont = self.italicAct.font()
        italicFont.setItalic(True)
        self.italicAct.setFont(italicFont)

        self.setLineSpacingAct = QAction("Set &Line Spacing...", self,
            statusTip="Change the gap between the lines of a paragraph",
            triggered=self.setLineSpacing)

        self.setParagraphSpacingAct = QAction("Set &Paragraph Spacing...",
            self, statusTip="Change the gap between paragraphs",
            triggered=self.setParagraphSpacing)

        self.aboutAct = QAction("&About", self,
            statusTip="Show the application's About box",
            triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
            statusTip="Show the Qt library's About box",
            triggered=self.aboutQt)
        self.aboutQtAct.triggered.connect(QApplication.instance().aboutQt)

        self.leftAlignAct = QAction("&Left Align", self, checkable=True,
            shortcut="Ctrl+L", statusTip="Left align the selected text",
            triggered=self.leftAlign)

        self.rightAlignAct = QAction("&Right Align", self, checkable=True,
            shortcut="Ctrl+R", statusTip="Right align the selected text",
            triggered=self.rightAlign)

        self.justifyAct = QAction("&Justify", self, checkable=True,
            shortcut="Ctrl+J", statusTip="Justify the selected text",
            triggered=self.justify)

        self.centerAct = QAction("&Center", self, checkable=True,
            shortcut="Ctrl+C", statusTip="Center the selected text",
            triggered=self.center)

        self.alignmentGroup = QActionGroup(self)
        self.alignmentGroup.addAction(self.leftAlignAct)
        self.alignmentGroup.addAction(self.rightAlignAct)
        self.alignmentGroup.addAction(self.justifyAct)
        self.alignmentGroup.addAction(self.centerAct)
        self.leftAlignAct.setChecked(True)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.formatMenu = self.editMenu.addMenu("&Format")
        self.formatMenu.addAction(self.boldAct)
        self.formatMenu.addAction(self.italicAct)
        self.formatMenu.addSeparator().setText("Alignment")
        self.formatMenu.addAction(self.leftAlignAct)
        self.formatMenu.addAction(self.rightAlignAct)
        self.formatMenu.addAction(self.justifyAct)
        self.formatMenu.addAction(self.centerAct)
        self.formatMenu.addSeparator()
        self.formatMenu.addAction(self.setLineSpacingAct)
        self.formatMenu.addAction(self.setParagraphSpacingAct)

    def closeEvent(self, event):
#        #if reactor.running:
#        #    reactor.stop()
         QCoreApplication.instance().quit()


if __name__ == '__main__':
    def _later():
        print("hello twisted")

    def stop():
        # Cleans up any protocol or spawned processes, if needed.
        print("Stop")
        if reactor.running:
            reactor.stop()

    app = QApplication(sys.argv)
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor

    if HAS_QDARKSTYLE:
        app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainWindow()
    window.show()
    # sys.exit(app.exec_())
    reactor.callLater(1.0, _later)
    # reactor.addSystemEventTrigger('before', 'shutdown', reactor.stop)
    app.lastWindowClosed.connect(stop)
    # print(dir(window))
    # window.closeEvent.connect(stop)
    reactor.run()
