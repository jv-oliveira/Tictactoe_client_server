# This Python file uses the following encoding: utf-8
import sys, os
from client.PlayerListModel import *
from client.local_game_manager import LocalGameManager
from client.server_comm import ServerComm
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType


if __name__ == "__main__":
    gameManager = LocalGameManager(None)
    playersListModel = gameManager.player_list_model
    # Set up the application window
    app = QGuiApplication(sys.argv)

    # playersListModel = PlayerListModel(None, )
    qmlRegisterType(ServerComm, 'Tictactoe', 1, 0, 'ServerComm')
    # qmlRegisterType(PlayerListModel, 'Tictactoe', 1, 0, 'PlayerListModel')
    qmlRegisterType(LocalGameManager, 'Tictactoe', 1, 0, 'GameManager')
    appDir = os.path.dirname(os.path.realpath(__file__))
    qml_file_app = os.path.join(appDir, "qml/app.qml")
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("applicationDirPath", os.path.dirname(os.path.realpath(__file__)))
    engine.rootContext().setContextProperty('gameManager', gameManager)
    engine.rootContext().setContextProperty('PlayerListModel', playersListModel)
    engine.rootContext().setContextProperty('serverComm', gameManager.server_comm)
    engine.rootContext().setContextProperty('MainWindow', engine)
    engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file_app)))

    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    #Show the window
    sys.exit(app.exec_())
