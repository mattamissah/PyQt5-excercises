import sys
from PyQt5.QtWidgets import *


class Form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.dial = QDial()
        self.dial.setNotchesVisible(True)
        self.spinBox = QSpinBox()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dial)
        self.layout.addWidget(self.spinBox)
        self.setLayout(self.layout)

        self.spinBox.valueChanged.connect(self.dial.setValue)
        self.dial.valueChanged.connect(self.spinBox.setValue)
        self.setWindowTitle('Signals and Slots')

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()