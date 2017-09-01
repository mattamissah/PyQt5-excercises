import sys
from math import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser = QTextBrowser()
        self.line_edit = QLineEdit("Type an expression & press Enter to solve ")
        self.line_edit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)
        self.line_edit.setFocus()
        self.line_edit.returnPressed.connect(self.updateUi)
        self.setWindowTitle("Calculate")

    def updateUi(self):
        try:
            text = self.line_edit.text()
            self.browser.append("%s = <b>%s</b>" % (text, eval(text)))
        except:
            self.browser.append("<font color=red>%s is invalid!</font>" % text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form =Form()
    form.show()
    app.exec_()