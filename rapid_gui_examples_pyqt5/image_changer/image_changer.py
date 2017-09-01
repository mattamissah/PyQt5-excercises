import os
import platform
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import rapid_gui_examples_pyqt5.image_changer.helpform
import rapid_gui_examples_pyqt5.image_changer.newimagedlg
import rapid_gui_examples_pyqt5.image_changer.qrc_resources

__version__ = "1.0.0"

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage()
        self.dirty = False
        self.filename = None
        self.morroredvertically = False
        self.mirriredhorizontally = False

        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.imageLabel)

        logDockWidget = QDockWidget("log", self)
        logDockWidget.setObjectName("logDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.listWidget = QListWidget()
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)

        self.printer = None

        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)

        self.fileNewAction = QAction(QIcon("pngs/document_new.png"), "&New", self)
        self.fileNewAction.setShortcut(QKeySequence.New)
        helpText = "Create a new image"
        self.fileNewAction.setToolTip(helpText)
        self.fileNewAction.setStatusTip(helpText)
        self.fileNewAction.triggered.connect(self.fileNew) # TODO

        self.fileMenu.addAction(self.fileNewAction)

    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        self.action = QAction(text, self)
        if icon is not None:
            self.action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            self.action.setShortcut(shortcut)
        if tip is not None:
            self.action.setToolTip(tip)
            self.action.setStatusTip(tip)
        if slot is not None:
            self.action.signal.connect(slot)
        if checkable:
            self.action.setCheckable(True)
        return self.action

