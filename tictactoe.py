import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView

myApp = QApplication(sys.argv)
print(os.path.dirname(os.path.realpath(__file__)) + "/images/board.png")
view = QQuickView()
view.rootContext().setContextProperty("applicationDirPath", os.path.dirname(os.path.realpath(__file__)))
view.setSource(QUrl('qml/tictactoe.qml'))
sys.exit(myApp.exec_())
