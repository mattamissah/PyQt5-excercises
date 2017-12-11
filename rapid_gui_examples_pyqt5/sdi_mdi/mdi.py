import sdi_mdi.textedit
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMdiArea
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import QFile, QSignalMapper, Qt, QSettings, QTimer


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        fileNewAction = self.createAction("&New", self.fileNew, QKeySequence.New, "filenew", "Create a text file")
        fileOpenAction = self.createAction("&Open", self.fileOpen,QKeySequence.Open, "fileopen",
                                           "Open an existing text file")
        fileSaveAction = self.createAction("&Save", self.fileSave, QKeySequence.Save, "filesave", "Save the text")
        fileSaveAsAction = self.createAction("Save &As...", self.fileSaveAs, icon="filesaveas",
                                             tip="Save the text using a new filename")
        fileSaveAllAction = self.createAction("Save A&ll", self.fileSaveAll, "filesave", tip="Save all the files")
        fileQuitAction = self.createAction("&Quit", self.close, "Ctrl+Q", "filequit", "Close the application")
        editCopyAction = self.createAction("&Copy", self.editCopy, QKeySequence.Copy, "editcopy",
                                           "Copy text to the clipboard")
        editCutAction = self.createAction("Cu&t", self.editCut, QKeySequence.Cut, "editcut","Cut text to the clipboard")
        editPasteAction = self.createAction("&Paste", self.editPaste, QKeySequence.Paste, "editpaste",
                                            "Paste in the clipboard's text")
        self.windowNextAction = self.createAction("&Next", self.mdi.activateNextWindow, QKeySequence.NextChild)
        self.windowPrevAction = self.createAction("&Previous", self.mdi.activatePreviousWindow,
                                                  QKeySequence.PreviousChild)
        self.windowCascadeAction = self.createAction("Casca&de",self.mdi.cascade)
        self.windowTileAction = self.createAction("&Tile",self.mdi.tile)
        self.windowRestoreAction = self.createAction("&Restore All",self.windowRestoreAll)
        self.windowMinimizeAction = self.createAction("&Iconize All",self.windowMinimizeAll)
        self.windowArrangeIconsAction = self.createAction("&Arrange Icons", self.mdi.arrangeIcons)
        self.windowCloseAction = self.createAction("&Close",self.mdi.closeActiveWindow, QKeySequence.Close)


        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped.connect(self.mdi.setActiveSubWindow())

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction, fileSaveAction, fileSaveAsAction, fileSaveAllAction,
                                   None, fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editCopyAction, editCutAction, editPasteAction))

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActions(editToolbar, (editCopyAction, editCutAction, editPasteAction))

        settings = QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry").toByteArray())
        self.restoreState(
            settings.value("MainWindow/State").toByteArray())

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        self.updateWindowMenu()
        self.setWindowTitle("Text Editor")
        QTimer.singleShot(0, self.loadFiles)

