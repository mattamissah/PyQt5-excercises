from PyQt5.QtWidgets import (QApplication, QListView, QStyledItemDelegate, QStyleOptionProgressBar,
                             QStyle, QSpinBox)
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant, QSortFilterProxyModel
from PyQt5.QtGui import QPainter

import sys

data = [70,80,90,99,90,80,70]

class PDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):

        item_var = index.data(Qt.DisplayRole)

        opts = QStyleOptionProgressBar()
        opts.rect = option.rect
        opts.minimum = 0
        opts.maximum = 100
        opts.text = str(item_var)
        opts.textAlignment = Qt.AlignCenter
        opts.textVisible = True
        opts.progress = int(item_var)

        QApplication.style().drawControl(QStyle.CE_ProgressBar, opts, painter)

class EDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        sbox = QSpinBox(parent)
        sbox.setRange(0, 100)
        return sbox

    def setEditorData(self, editor, index):
        item_var = index.data(Qt.DisplayRole)
        item_int = int(item_var)
        editor.setValue(item_int)

    def setModelData(self, editor, model, index):
        data = editor.value()
        data_var = QVariant(data)
        model.setData(index, data_var)


class SortProxy(QSortFilterProxyModel):
    def LessThan(self, left_index, right_index):
        left_var = left_index.data(Qt.DisplayRole)
        right_var = right_index.data(Qt.DisplayRole)

        left_int = left_var.value()
        right_int = right_var.value()
        print(type(left_int, right_int))
        return (left_int < right_int)


class FilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, src_row, src_parent):
        src_model = self.sourceModel()
        src_index = src_model.index(src_row, 0)
        item_var = src_index.data(Qt.DisplayRole)
        item_int = item_var.value()
        return (item_int >= 60)


class ListM(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return QVariant()
        row = index.row()

        if role == Qt.DisplayRole:
            return self._data[row]
        elif role == Qt.EditRole:
            return str(self._data[row])

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return QVariant()
        row = index.row()

        if role == Qt.EditRole:
            value_int = value
            if isinstance(value_int.value(), int):
                self._data[row] = value_int.value()
                self.dataChanged.emit(index, index)
                return True
            return False

    def flags(self, index):
        flag = super().flags(index)
        return flag | Qt.ItemIsEditable


app = QApplication(sys.argv)
a = ListM()
ap = SortProxy()
ap.setSourceModel(a)
ap.sort(0)

b = QListView()

b.setModel(ap)

b.show()

sys.exit(app.exec_())