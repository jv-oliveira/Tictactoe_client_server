# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import QAbstractListModel, Qt, pyqtSignal, pyqtSlot, QModelIndex

class PlayerListModel(QAbstractListModel):

    IDRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    GamingStateRole = Qt.UserRole + 3

    playerChanged = pyqtSignal()

    def __init__(self, parent=None, players=[]):
        super().__init__(parent)
        self._players = players

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if role == PlayerListModel.NameRole:
            return self._players[row]["name"]
        if role == PlayerListModel.IDRole:
            return self._players[row]["id"]
        if role == PlayerListModel.GamingStateRole:
            return self._players[row]["gamingState"]

    def rowCount(self, parent=QModelIndex()):
        return len(self._players)

    def roleNames(self):
        return {
            PlayerListModel.IDRole: b'id',
            PlayerListModel.NameRole: b'name',
            PlayerListModel.GamingStateRole: b'gamingState'
        }

    @pyqtSlot(int, str)
    def addPlayer(self, id: int, name: str):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._players.append({'id': id, 'name': name, 'gamingState': 0})
        self.endInsertRows()

    @pyqtSlot(int, int, str, int)
    def insertPlayer(self, row: int, id: int, name: str, gamingState: int):
        self.beginInsertRows(QModelIndex(), row, row)
        self._players.insert(row, {'id': id, 'name': name, 'gamingState': gamingState})
        self.endInsertRows()

    @pyqtSlot(int, int, str, int)
    def editPlayer(self, row: int, id: int, name: str, gamingState: int):
        ix = self.index(row, 0)
        self._players[row] = {'id': id, 'name': name, 'gamingState': gamingState}
        self.dataChanged.emit(ix, ix, self.roleNames())

    @pyqtSlot(int)
    def deletePlayer(self, row):
        self.beginRemoveColumns(QModelIndex(), row, row)
        del self._players[row]
        self.endRemoveRows()
