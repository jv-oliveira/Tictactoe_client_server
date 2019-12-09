import QtQuick 2.13

Item {
    id: container
    width: 350
    height: 500

    property string playerName: ""
    property int playerID: 0

    Column {
        topPadding: 100
        spacing: 100

        Text {
            id: textEdit
            x: 60
            y: 150
            width: 233
            height: 50
            text: container.playerName + " ( ID: " + container.playerID.toString(
                      ) + " )\n quer jogar. Aceita?"
            font.pixelSize: 24
        }

        Row {
            leftPadding: 20
            rightPadding: 20
            spacing: 100
            Button {
                id: okButton
                text: "OK"
                onClicked: okButton.pressed = true
                onReleased: {
                    okButton.pressed = false
                    gameManager.acceptInvite(true)
                }
            }

            Button {
                id: cancelButton
                text: "Recusar"
                onClicked: cancelButton.pressed = true
                onReleased: {
                    cancelButton.pressed = false
                    gameManager.acceptInvite(false)
                }
            }
        }
    }
}
