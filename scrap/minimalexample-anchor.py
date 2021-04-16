import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

class MyTextEdit(QtWidgets.QTextEdit):
    def contextMenuEvent(self, event):
        anchor = self.anchorAt(event.pos())
        if len(anchor) > 0:
            QtWidgets.QMessageBox.information(self, "Anchor Found", "The anchor {} was found".format(anchor))

app = QtWidgets.QApplication([])
textEdit = MyTextEdit()
textEdit.insertHtml('&lt;<a href="test1">test1</a>&gt;')
textEdit.insertPlainText("test2")
textEdit.show()
app.exec()