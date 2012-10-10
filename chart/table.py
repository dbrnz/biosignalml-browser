"""
A generic widget and model for working with a table view.

Selection by row and sortable columns are provided.
"""

from PyQt4 import QtCore, QtGui


class TableView(QtGui.QTableView):
#=================================
  """
  A generic table view.
  """

  def __init__(self, *args, **kwds):
  #---------------------------------
    QtGui.QTableView.__init__(self, *args, **kwds)
    self.setAlternatingRowColors(True)
    self.setShowGrid(False)
    self.setWordWrap(True)
    self.setSortingEnabled(True)
    self.verticalHeader().setVisible(False)
    self.horizontalHeader().setStretchLastSection(True)
    self.horizontalHeader().setHighlightSections(False)
    self.horizontalHeader().setSortIndicatorShown(True)
    self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

  def resizeCells(self):  # Needs to be done after table is populated
  #---------------------
    selected = self.selectedIndexes()
    self.hide()
    self.resizeColumnsToContents()
    self.show()
    self.hide()
    self.resizeRowsToContents()
    if selected: self.selectRow(selected[0].row())
    self.show()


class TableModel(QtCore.QAbstractTableModel):
#============================================
  """
  A generic table model.

  :param header (list): A list of column headings.
  :param rows (list): A list of table data rows, with each element
     a list of the row's column data.
  """

  def __init__(self, header, rows, parent=None):
  #---------------------------------------------
    QtCore.QAbstractTableModel.__init__(self, parent)
    self._header = header
    self._rows = rows

  def rowCount(self, parent=None):
  #-------------------------------
    return len(self._rows)

  def columnCount(self, parent=None):
  #----------------------------------
    return len(self._header)

  def headerData(self, section, orientation, role):
  #------------------------------------------------
    if orientation == QtCore.Qt.Horizontal:
      if role == QtCore.Qt.DisplayRole:
        return self._header[section]
      elif role == QtCore.Qt.TextAlignmentRole:
        return QtCore.Qt.AlignLeft
      elif role == QtCore.Qt.FontRole:
        font = QtGui.QFont(QtGui.QApplication.font())
        font.setBold(True)
        return font

  def data(self, index, role):
  #---------------------------
    if   role == QtCore.Qt.DisplayRole:
      value = self._rows[index.row()][index.column()]
      return QtCore.QVariant(value) if value is not None else ''
    elif role == QtCore.Qt.TextAlignmentRole:
      return QtCore.Qt.AlignTop

  def flags(self, index):
  #-----------------------
    return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

  def appendRows(self, rows):
  #--------------------------
    posns = (len(self._rows), len(self._rows) + len(rows) - 1)
    self.beginInsertRows(self.createIndex(len(self._rows), 0), posns[0], posns[1])
    self._rows.extend(rows)
    self.endInsertRows()
    return posns

  def removeRows(self, posns):
  #---------------------------
    self.beginRemoveRows(self.createIndex(posns[0], 0), posns[0], posns[1])
    self._rows[posns[0]:posns[1]+1] = []
    self.endRemoveRows()


class SortedTable(QtGui.QSortFilterProxyModel):
#==============================================
  """
  A generic sorted table.

  :param header (list): A list of column headings.
  :param rows (list): A list of table data rows, with each element
     a list of the row's column data.
  """

  def __init__(self, header, rows, tablefilter=None, parent=None):
  #---------------------------------------------------------------
    QtGui.QSortFilterProxyModel.__init__(self, parent)
    self._table = TableModel(header, rows, parent)
    self.setSourceModel(self._table)

#    self._filter = tablefilter    # function(row, content)
#
#  def setFilter(self, tablefilter):
#  #--------------------------------
#    self._table.layoutAboutToBeChanged.emit()
#    self._filter = tablefilter    # function(row, content)
#    self._table.layoutChanged.emit()
#
#  def clearFilter(self):
#  #---------------------
#    self._table.layoutAboutToBeChanged.emit()
#    self._filter = None
#    self._table.layoutChanged.emit()
#
#  def filterAcceptsRow(self, row, source):
#  #---------------------------------------
#    return (self._filter is None
#         or self._filter(row, self._table._rows[row]))

  def appendRows(self, rows):
  #--------------------------
    self._table.layoutAboutToBeChanged.emit()
    posns = self._table.appendRows(rows)
    self._table.layoutChanged.emit()
    return posns

  def removeRows(self, posns):
  #---------------------------
    self._table.layoutAboutToBeChanged.emit()
    self._table.removeRows(posns)
    self._table.layoutChanged.emit()
