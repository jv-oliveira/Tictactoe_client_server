import QtQuick 2.4

Item {
    width: 350
    height: 500

    Text {
        id: textEdit
        x: 60
        y: 150
        width: 233
        height: 50
        text: qsTr("Insira aqui seu nome:")
        font.pixelSize: 24
    }

    Rectangle {
        id: rectangle
        x: 60
        y: 250
        width: 235
        height: 54
        color: "#00000000"
        radius: 5
        border.width: 5

        TextInput {
            id: textInput
            x: 60
            y: 250
            height: 40
            text: qsTr("Nome")
            anchors.rightMargin: -105
            anchors.leftMargin: -105
            anchors.top: parent.verticalCenter
            anchors.right: parent.horizontalCenter
            anchors.bottom: parent.verticalCenter
            anchors.left: parent.horizontalCenter
            anchors.bottomMargin: -17
            anchors.topMargin: -17
            passwordCharacter: "\u2022"
            font.pixelSize: 24
        }
    }

    Button {
        id: nextButton
        text: "próximo"
        anchors.top: rectangle.bottom
        anchors.topMargin: 20
        anchors.left: parent.left
        anchors.leftMargin: 50
        onClicked: nextButton.pressed = true
        onReleased: {
            nextButton.pressed = false
            gameManager.tryLogin(textInput.text.toString())
        }
    }
}
