import sys
from PyQt5.QtWidgets import *

class Form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.btn1 = QPushButton("One")
        self.btn2 = QPushButton("Two")
        self.btn3 = QPushButton("Three")
        self.btn4 = QPushButton("Four")
        self.btn5 = QPushButton("Five")
        self.label = QLabel()
        layout = QHBoxLayout()

        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        layout.addWidget(self.btn4)
        layout.addWidget(self.btn5)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.btn1.clicked.connect(self.da_slot)
        self.btn2.clicked.connect(self.da_slot)  # will use sender() to access sender text
        self.btn3.clicked.connect(self.da_slot)
        self.btn4.clicked.connect(lambda:  self.da_slot("Four")) # using lambda to pass msg from sender
        self.btn5.clicked.connect(lambda:  self.da_slot("Five"))

    def da_slot(self, btn=None):
        button = self.sender()
        if btn is not None:
            self.label.setText("You clicked button {}".format(button.text()))
        else:
            self.label.setText("You have clicked button {}".format(btn))

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()