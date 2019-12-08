import QtQuick 2.13
import QtQuick.Controls 1.4
import "../qml"

ApplicationWindow {
    id: window
    visible: true
    title: "Jogo da Velha"

    ServerForm {
        id: serverForm

        onServerConnect: {
            serverForm.visible = false
            playersListForm.visible = true
        }
    }

    PlayerListForm {
        id: playersListForm
        visible: false
    }


}
