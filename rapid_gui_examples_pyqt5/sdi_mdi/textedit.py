from PyQt5.QtWidgets import  QFileDialog, QTextEdit, QMessageBox
from PyQt5.QtCore import QFile, Qt, QFileInfo, QIODevice, QTextStream

class TextEdit(QTextEdit):
    NextId = 1

    def __init__(self, filename='', parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.filename = filename
        if not self.filename:
            self.filename = 'Untitled-{0}.txt'.format(TextEdit.NextId)
            TextEdit.NextId += 1
        self.document().setModified(False)
        self.setWindowTitle(QFileInfo(self.filename).fileName())


    def isModified(self):
        return self.document().isModified()

    def save(self):
        if self.filename.endswith('Untitled.txt'):
            filename, _ = QFileDialog.getSaveFileName(self, "Text Editor --Save File As", self.filename,
                                                   'Text files (*.txt)')
            if not filename:
                return
            self.filename = filename
        self.setWindowTitle(QFileInfo(self.filename).filename())
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.toPlainText()
            self.document().setModified(False)
        except (IOError, OSError) as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception

    def closeEvent(self, event):
        if (self.document().isModified() and QMessageBox.question(self,"Text Editor - Unsaved Changes",
                                         "Save unsaved changes in {0}?".format(self.filename),
                                         QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
            try:
                self.save()
            except (IOError, OSError) as e:
                QMessageBox.warning(self,"Text Editor -- Save Error","Failed to save {0}: {1}".format(self.filename, e))

    def load(self):
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            self.setPlainText(stream.readAll())
            self.document().setModified(False)
        except (IOError, OSError) as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception