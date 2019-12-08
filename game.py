from PyQt5.QtCore import pyqtProperty, QObject


class Game(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self ._board = []


