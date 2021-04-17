import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

class MyTextEdit(QtWidgets.QTextEdit):
    def contextMenuEvent(self, event):
        anchor = self.anchorAt(event.pos())
        if len(anchor) > 0:
            QtWidgets.QMessageBox.information(self, "Anchor Found", "The anchor {} was found".format(anchor))

app = QtWidgets.QApplication([])
textEdit = MyTextEdit()
textEdit.setHtml('<a href="first">&lt;user1&gt;</a> first user<br><a href="second">&lt;second&gt;</a> second user')
textEdit.show()
app.exec()