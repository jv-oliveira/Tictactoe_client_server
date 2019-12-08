from PyQt5.QtCore import pyqtProperty, QObject
from enum import Enum


class Symbols(Enum):
    CROSS = 'X'
    CIRCLE = 'O'


class LocalGameManager(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self._player_symbol = None
        self._running = False

    @pyqtProperty('Qstring')
    def player_symbol(self):
        return self._player_symbol

    @player_symbol.setter
    def player_symbol(self, player_symbol: str):
        if player_symbol in Symbols:
            self._player_symbol = player_symbol

    @pyqtProperty(bool)
    def running(self):
        return self._running

    @running.setter
    def running(self, value: bool):
        self._running = value

