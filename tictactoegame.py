# This Python file uses the following encoding: utf-8
import sys, os
from PlayerListModel import *
from PlayerStates import States
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine


if __name__ == "__main__":

    playersListModel = PlayerListModel(None, [
        {'id': 1, 'name': 'João', 'gamingState': 0},
        {'id': 2, 'name': 'Pedro', 'gamingState': 0},
        {'id': 3, 'name': 'Carla', 'gamingState': 0},
        {'id': 4, 'name': 'Letícia', 'gamingState': 0}
    ])
    #Set up the application window
    app = QGuiApplication(sys.argv)

    appDir = os.path.dirname(os.path.realpath(__file__))
    qml_file_app = os.path.join(appDir, "qml/app.qml")
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("applicationDirPath", os.path.dirname(os.path.realpath(__file__)))
    engine.rootContext().setContextProperty('PlayerListModel', playersListModel)
    engine.rootContext().setContextProperty('MainWindow', engine)
    engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file_app)))

    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    #Show the window
    sys.exit(app.exec_())
