# !/usr/bin/python
# -*- coding: utf-8 -*-

""""pyforms.gui.Controls.Control Tree"""

from pyforms.gui.Controls.ControlBase import ControlBase
from PyQt4.QtGui import QTreeWidget, QTreeWidgetItem, QTreeView
from PyQt4.QtGui import QAbstractItemView

__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Ricardo Ribeiro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlTree(ControlBase, QTreeWidget):
    """This class represents a wrapper to the QTreeWidget"""

    def __init__(self, label='', default=''):
        QTreeWidget.__init__(self)
        ControlBase.__init__(self, label, default)
        

    def initForm(self):
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setUniformRowHeights(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)

        self.model().dataChanged.connect(self.__itemChangedEvent)

        self.selectionChanged = self.selectionChanged

    @property
    def showHeader(self):
        return self.header().isVisible()

    @showHeader.setter
    def showHeader(self, value):
        if value:
            self.header().show()
        else:
            self.header().hide()

    def __itemChangedEvent(self, item): self.itemChangedEvent(item)

    def itemChangedEvent(self, item): pass

    def itemSelectionChanged(self): pass

    def rowsInsertedEvent(self, parent, start, end):
        """ This event is called every time a new row is added to the tree"""
        pass

    def rowsInserted(self, parent, start, end):
        super(ControlTree, self).rowsInserted(parent, start, end)
        self.rowsInsertedEvent(parent, start, end)

    def selectionChanged(self, selected, deselected):
        super(QTreeView, self).selectionChanged(selected, deselected)
        self.itemSelectionChanged()

    @property
    def mouseSelectedRowsIndexes(self):
        result = []
        for index in self.selectedIndexes():
            result.append(index.row())
        return list(set(result))

    @property
    def mouseSelectedRowIndex(self):
        indexes = self.mouseSelectedRowsIndexes
        if len(indexes) > 0:
            return indexes[0]
        else:
            return None

    @property
    def selectedItem(self):
        for index in self.selectedIndexes():
            item = index.model().itemFromIndex(index)
            return item
        else:
            return None

    @property
    def cells(self):
        results = []
        for row in range(self.model().rowCount()):
            r = []
            for col in range(self.model().columnCount()):
                r.append(self.model.item(row, col))

            if len(r) > 0:
                results.append(r)

        return results

    def __add__(self, other):
        if isinstance(other, QTreeWidgetItem):
            self.model().invisibleRootItem().appendRow(other)

        elif isinstance(other, list):
            for x in other:
                item = QTreeWidgetItem(x)
                self.form.addTopLevelItem(item)
        else:
            item = QTreeWidgetItem(other)
            self.form.addTopLevelItem(item)

        self.setFirstColumnSpanned(
            self.model().rowCount() - 1, self.rootIndex(), True)
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            if other < 0:
                indexToRemove = self.mouseSelectedRowIndex
            else:
                indexToRemove = other
            self.model().removeRow(indexToRemove)
        return self

    @property
    def form(self): return self

    @property
    def value(self): return None

    @value.setter
    def value(self, value): self.addTopLevelItem(value)

    def save(self, data): pass

    def load(self, data): pass
