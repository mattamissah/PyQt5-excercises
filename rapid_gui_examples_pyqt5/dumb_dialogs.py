import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.width = 1
        self.beveled = False
        self.style = "Solid"

        self.penButtonInline = QPushButton("Set Pen... (Dumb &inline)")
        self.penButton = QPushButton("Set Pen... (Dumb &class)")
        self.label = QLabel("The Pen has not been set")
        self.label.setTextFormat(Qt.RichText)

        layout = QVBoxLayout()
        layout.addWidget(self.penButtonInline)
        layout.addWidget(self.penButton)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.penButtonInline.clicked.connect(self.setPenInline)
        self.penButton.clicked.connect(self.setPenProperties)
        self.setWindowTitle("Pen")
        self.updateData()


    def updateData(self):
        bevel = ""
        if self.beveled:
            bevel = "<br>Beveled"
        self.label.setText("Width = %d<br>Style = %s%s" % (self.width, self.style, self.beveled))


    def setPenProperties(self):
        dialog = PenPropertiesDlg(self)
        dialog.widthSpinBox.setValue(self.width)
        dialog.beveledCheckBox.setChecked(self.beveled)
        dialog.styleComboBox.setCurrentIndex(dialog.styleComboBox.findText(self.style))

        if dialog.exec_():
            self.width = dialog.widthSpinBox.value()
            self.beveled = dialog.beveledCheckBox.isChecked()
            self.style = dialog.styleComboBox.currentText()
            self.updateData()

    def setPenInline(self):
        widthLabel = QLabel("&Width:")
        widthSpinBox = QSpinBox()
        widthLabel.setBuddy(widthSpinBox)
        widthSpinBox.setAlignment(Qt.AlignRight)
        widthSpinBox.setRange(0, 24)
        widthSpinBox.setValue(self.width)
        beveledCheckBox = QCheckBox("&Beveled edges")
        beveledCheckBox.setChecked(self.beveled)
        styleLabel = QLabel("&Style:")
        styleComboBox = QComboBox()
        styleLabel.setBuddy(styleComboBox)
        styleComboBox.addItems(["Solid", "Dashed", "Dotted", "DashDotted", "DashDotDotted"])
        styleComboBox.setCurrentIndex(styleComboBox.findText(self.style))
        self.okButton = QPushButton("&OK")
        self.cancelButton = QPushButton("Cancel")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        layout = QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(widthSpinBox, 0, 1)
        layout.addWidget(beveledCheckBox, 0, 2)
        layout.addWidget(styleLabel, 1, 0)
        layout.addWidget(styleComboBox, 1, 1, 1, 2)
        layout.addLayout(buttonLayout, 2, 0, 1, 3)

        form = QDialog()
        form.setLayout(layout)
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        form.setWindowTitle("Pen Properties")

        if form.exec_():
            self.width = widthSpinBox.value()
            self.beveled = beveledCheckBox.isChecked()
            self.style = styleComboBox.currentText()
            self.updateData()


class PenPropertiesDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        widthLabel = QLabel("&Width:")
        self.widthSpinBox = QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.widthSpinBox.setRange(0, 24)
        self.beveledCheckBox = QCheckBox("&Beveled edges")
        styleLabel = QLabel("&Style:")
        self.styleComboBox = QComboBox()
        styleLabel.setBuddy(self.styleComboBox)
        self.styleComboBox.addItems(["Solid", "Dashed", "Dotted", "DashDotted", "DashDotDotted"])
        self.okButton = QPushButton("&OK")
        self.cancelButton = QPushButton("Cancel")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        layout = QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(self.beveledCheckBox, 0, 2)
        layout.addWidget(styleLabel, 1, 0)
        layout.addWidget(self.styleComboBox, 1, 1, 1, 2)
        layout.addLayout(buttonLayout, 2, 0, 1, 3)
        self.setLayout(layout)

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self.setWindowTitle("Pen Properties")

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
