import os
import platform
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from image_changer.helpform import HelpForm
from image_changer.newimagedlg import NewImgDlg
import image_changer.qrc_resources

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

        # self.fileNewAction = QAction(QIcon("pngs/document_new.png"), "&New", self)
        # self.fileNewAction.setShortcut(QKeySequence.New)
        # helpText = "Create a new image"
        # self.fileNewAction.setToolTip(helpText)
        # self.fileNewAction.setStatusTip(helpText)
        # self.fileNewAction.triggered.connect(self.fileNew)

        # Menu Actions
        fileNewAction = self.createAction("&New...", self.fileNew, QKeySequence.New, "pngs/document_new.png",
                                          "Create a new image file")  # TODO fileNew method
        fileOpenAction = self.createAction("&Open...", self.fileOpen, QKeySequence.Open, tip="Open existing image file")
        fileSaveAction = self.createAction("&Save", self.fileSave, QKeySequence.Save, "pngs/save.png",
                                           "Save changes")
        fileSaveAsAction = self.createAction("Save &As...", self.fileSaveAs)
        filePrintAction = self.createAction("&Print", self.filePrint, QKeySequence.Print, "pngs/print.png")
        fileQuitAction = self.createAction("&Quit", self.close, "Ctrl+Q", tip="save and exit app")

        invertEditAction = self.createEditAction("&invert", self.editInvert, "Ctrl+I", tip="Invert the image's colors",
                                             checkable=True)  # signal "toggled(bool)"
        swapRedBlueEditAction = self.createEditAction("Sw&ap red and blue", self.editSwapRedAndBlue, "Ctrl+A",
                                                        tip="swap the images' red and blue components", checkable=True)
        zoomEditAction = self.createEditAction("&Zoom...", self.editZoom, "Alt+Z", "pngs/zoom.png", tip="zoom image")

        mirrorGroup = QActionGroup(self)
        unMirrorEditAction = self.createEditAction("&Unmirror", self.editUnMirror, "Ctrl+U", tip="Unmirror the image",
                                                   checkable=True)
        mirrorGroup.addAction(unMirrorEditAction)
        mirrorHorizontalEditAction = self.createEditAction("Mirror &Horizontally", self.editMirrorHorizontal, "ctrl+V",
                                                           tip="Horizontal mirror", checkable=True)
        mirrorGroup.addAction(mirrorHorizontalEditAction)
        mirrorVerticalEditAction = self.createEditAction("Mirror &Vertically", self.editMirrorVertical, "ctrl+H",
                                                           tip="Vertical mirror", checkable=True)
        mirrorGroup.addAction(mirrorVerticalEditAction)

        unMirrorEditAction.setChecked(True)

        helpAboutAction = self.createAction("&About", self.helpAbout)
        helpHelpAction = self.createAction("&Help", self.helpHelp, QKeySequence.HelpContents)

        # Menus
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuActions = (fileNewAction, fileOpenAction, fileSaveAction, fileSaveAsAction, None,
                                filePrintAction, fileQuitAction)
        self.fileMenu.aboutToShow.connect(self.updateFileMenu)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(self.editMenu, (invertEditAction, swapRedBlueEditAction, zoomEditAction))

        self.mirrorMenu = self.editMenu.addMenu(QIcon("pngs/editmirror.png"), "&Mirror")
        self.addActions(self.mirrorMenu, (unMirrorEditAction, mirrorHorizontalEditAction, mirrorVerticalEditAction))

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(self.helpMenu, (helpAboutAction,helpHelpAction))

        # Toolbars
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction, fileSaveAsAction))

        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (invertEditAction, swapRedBlueEditAction, unMirrorEditAction,
                                      mirrorVerticalEditAction, mirrorHorizontalEditAction))

        self.zoomSpinBox = QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("Zoom the image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)
        self.zoomSpinBox.valueChanged.connect(self.showImage)  # TODO
        editToolbar.addWidget(self.zoomSpinBox)

        self.addActions(self.imageLabel, (invertEditAction, swapRedBlueEditAction, unMirrorEditAction,
                                          mirrorVerticalEditAction, mirrorHorizontalEditAction))

        self.resetableActions = ( (invertEditAction, False), (swapRedBlueEditAction, False),
                                  (unMirrorEditAction, True))

        settings =QSettings()
        self.recentFiles = settings.value("RecentFiles").toStringList()
        self.restoreGeometry(settings.value("MainWindow/Geometry").toByteArray())
        self.restoreState(settings.value("MainWindow/State").toByteArray())

        self.setWindowTitle("Image Changer")
        self.updateFileMenu()

        QTimer.singleShot(0, self.loadInitialFile)

    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False):
        self.action = QAction(text, self)
        if icon is not None:
            self.action.setIcon(QIcon("icon"))
        if shortcut is not None:
            self.action.setShortcut(shortcut)
        if tip is not None:
            self.action.setToolTip(tip)
            self.action.setStatusTip(tip)
        if slot is not None:
            self.action.triggered.connect(slot)
        if checkable:
            self.action.setCheckable(True)
        return self.action

    def createEditAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False):
        self.action = QAction(text, self)
        if icon is not None:
            self.action.setIcon(QIcon("icon"))
        if shortcut is not None:
            self.action.setShortcut(shortcut)
        if tip is not None:
            self.action.setToolTip(tip)
            self.action.setStatusTip(tip)
        if slot is not None:
            self.action.toggled.connect(slot)
        if checkable:
            self.action.setCheckable(True)
        return self.action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            filename = (QVariant(self.filename)
                        if self.filename is not None else QVariant())
            settings.setValue("LastFile", filename)
            recentFiles = (QVariant(self.recentFiles)
                           if self.recentFiles else QVariant())
            settings.setValue("RecentFiles", recentFiles)
            settings.setValue("MainWindow/Geometry", QVariant(
                self.saveGeometry()))
            settings.setValue("MainWindow/State", QVariant(
                self.saveState()))
        else:
            event.ignore()

    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self,
                                         "Image Changer - Unsaved Changes",
                                         "Save unsaved changes?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True

    def loadInitialFile(self):
        settings = QSettings()
        fname = settings.value("LastFile").toString()
        if fname and QFile.exists(fname):
            self.loadFile(fname)

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        self.listWidget.addItem(message)
        if self.filename is not None:
            self.setWindowTitle("Image Changer - {0}[*]".format(
                os.path.basename(self.filename)))
        elif not self.image.isNull():
            self.setWindowTitle("Image Changer - Unnamed[*]")
        else:
            self.setWindowTitle("Image Changer[*]")
        self.setWindowModified(self.dirty)

    def updateFileMenu(self):
        self.fileMenu.clear()
        self.addActions(self.fileMenu, self.fileMenuActions[:-1])
        current = self.filename if self.filename is not None else None
        recentFiles = []
        for fname in self.recentFiles:
            if fname != current and QFile.exists(fname):
                recentFiles.append(fname)
        if recentFiles:
            self.fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                action = QAction(QIcon(":/icon.png"),
                                 "&{0} {1}".format(i + 1, QFileInfo(
                                     fname).fileName()), self)
                action.setData(QVariant(fname))
                self.action.triggered.connect(self.loadFile)
                self.fileMenu.addAction(action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileMenuActions[-1])

    def fileNew(self):
        if not self.okToContinue():
            return
        dialog = NewImgDlg(self)
        if dialog.exec_():
            self.addRecentFile(self.filename)
            self.image = QImage()
            for action, check in self.resetableActions:
                action.setChecked(check)
            self.image = dialog.image()
            self.filename = None
            self.dirty = True
            self.showImage()
            self.sizeLabel.setText("{0} x {1}".format(self.image.width(),
                                                      self.image.height()))
            self.updateStatus("Created new image")

    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        formats = (["*.{0}".format(format.lower())
                    for format in QImageReader.supportedImageFormats()])
        fname = QFileDialog.getOpenFileName(self,
                                                    "Image Changer - Choose Image", dir,
                                                    "Image files ({0})".format(" ".join(formats)))
        if fname:
            self.loadFile(fname)

    def loadFile(self, fname=None):
        if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = action.data().toString()
                if not self.okToContinue():
                    return
            else:
                return
        if fname:
            self.filename = None
            image = QImage(fname)
            if image.isNull():
                message = "Failed to read {0}".format(fname)
            else:
                self.addRecentFile(fname)
                self.image = QImage()
                for action, check in self.resetableActions:
                    action.setChecked(check)
                self.image = image
                self.filename = fname
                self.showImage()
                self.dirty = False
                self.sizeLabel.setText("{0} x {1}".format(
                    image.width(), image.height()))
                message = "Loaded {0}".format(os.path.basename(fname))
            self.updateStatus(message)

    def addRecentFile(self, fname):
        if fname is None:
            return
        if not self.recentFiles.contains(fname):
            self.recentFiles.prepend(fname)
            while self.recentFiles.count() > 9:
                self.recentFiles.takeLast()

    def fileSave(self):
        if self.image.isNull():
            return True
        if self.filename is None:
            return self.fileSaveAs()
        else:
            if self.image.save(self.filename, None):
                self.updateStatus("Saved as {0}".format(self.filename))
                self.dirty = False
                return True
            else:
                self.updateStatus("Failed to save {0}".format(
                    self.filename))
                return False

    def fileSaveAs(self):
        if self.image.isNull():
            return True
        fname = self.filename if self.filename is not None else "."
        formats = (["*.{0}".format(format).lower()
                    for format in QImageWriter.supportedImageFormats()])
        fname = QFileDialog.getSaveFileName(self,
                                                    "Image Changer - Save Image", fname,
                                                    "Image files ({0})".format(" ".join(formats)))
        if fname:
            if "." not in fname:
                fname += ".png"
            self.addRecentFile(fname)
            self.filename = fname
            return self.fileSave()
        return False

    def filePrint(self):
        if self.image.isNull():
            return
        if self.printer is None:
            self.printer = QPrinter(QPrinter.HighResolution)
            self.printer.setPageSize(QPrinter.Letter)
        form = QPrintDialog(self.printer, self)
        if form.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(),
                                size.height())
            painter.drawImage(0, 0, self.image)

    def editInvert(self, on):
        if self.image.isNull():
            return
        self.image.invertPixels()
        self.showImage()
        self.dirty = True
        self.updateStatus("Inverted" if on else "Uninverted")

    def editSwapRedAndBlue(self, on):
        if self.image.isNull():
            return
        self.image = self.image.rgbSwapped()
        self.showImage()
        self.dirty = True
        self.updateStatus(("Swapped Red and Blue"
                           if on else "Unswapped Red and Blue"))

    def editUnMirror(self, on):
        if self.image.isNull():
            return
        if self.mirroredhorizontally:
            self.editMirrorHorizontal(False)
        if self.mirroredvertically:
            self.editMirrorVertical(False)

    def editMirrorHorizontal(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(True, False)
        self.showImage()
        self.mirroredhorizontally = not self.mirroredhorizontally
        self.dirty = True
        self.updateStatus(("Mirrored Horizontally"
                           if on else "Unmirrored Horizontally"))

    def editMirrorVertical(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(False, True)
        self.showImage()
        self.mirroredvertically = not self.mirroredvertically
        self.dirty = True
        self.updateStatus(("Mirrored Vertically"
                           if on else "Unmirrored Vertically"))

    def editZoom(self):
        if self.image.isNull():
            return
        percent, ok = QInputDialog.getInteger(self,
                                              "Image Changer - Zoom", "Percent:",
                                              self.zoomSpinBox.value(), 1, 400)
        if ok:
            self.zoomSpinBox.setValue(percent)

    def showImage(self, percent=None):
        if self.image.isNull():
            return
        if percent is None:
            percent = self.zoomSpinBox.value()
        factor = percent / 100.0
        width = self.image.width() * factor
        height = self.image.height() * factor
        image = self.image.scaled(width, height, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        # According to PyQt's documentation, QPixmaps are optimized for on-screen
        # display (so they are fast to draw), and QImages are optimized for editing (which is why we have used them to hold the image data).

    def helpAbout(self):
        QMessageBox.about(self, "About Image Changer",
                          """<b>Image Changer</b> v {0}
                          <p>Copyright &copy; 2008 Qtrac Ltd. 
                          All rights reserved.
                          <p>This application can be used to perform
                          simple image manipulations.
                          <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                              __version__, platform.python_version(),
                              QT_VERSION_STR, PYQT_VERSION_STR,
                              platform.system()))

    def helpHelp(self):
        form = HelpForm("index.html", self)
        form.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()