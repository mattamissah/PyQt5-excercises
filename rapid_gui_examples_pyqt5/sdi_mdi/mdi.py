from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMdiArea
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFile

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mdi = QMdiArea()
