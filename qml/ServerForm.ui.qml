import QtQuick 2.4

import "../qml"

Item {
    id: container
    width: 350
    height: 500

    signal serverConnect

    Text {
        id: textEdit
        x: 50
        y: 46
        width: 300
        height: 50
        text: qsTr("Conecte ao servidor!")
        font.pixelSize: 24
    }

    Text {
        id: textEdit1
        x: 50
        y: 145
        width: 300
        height: 24
        text: qsTr("IP")
        font.pixelSize: 24
    }

    Rectangle {
        id: rectangle
        x: 50
        y: 183
        width: 235
        height: 54
        color: "#00000000"
        radius: 5
        border.width: 5

        TextInput {
            id: textInput
            x: 15
            height: 40
            text: qsTr("IP")
            anchors.rightMargin: -105
            anchors.leftMargin: -105
            anchors.top: parent.verticalCenter
            anchors.right: parent.horizontalCenter
            anchors.bottom: parent.verticalCenter
            anchors.left: parent.horizontalCenter
            anchors.bottomMargin: -17
            anchors.topMargin: -17
            inputMask: "000.000.000.000;_"
            passwordCharacter: "\u2022"
            font.pixelSize: 24
        }
    }

    Text {
        id: textEdit2
        x: 50
        y: 270
        width: 300
        height: 24
        text: qsTr("Porta")
        font.pixelSize: 24
    }

    Rectangle {
        id: rectangle1
        x: 50
        y: 300
        width: 235
        height: 54
        color: "#00000000"
        radius: 5
        border.width: 5

        TextInput {
            id: textInput2
            width: 80
            height: 40
            text: qsTr("Porta")
            anchors.rightMargin: 24
            anchors.leftMargin: -103
            anchors.bottomMargin: -19
            anchors.top: parent.verticalCenter
            anchors.right: parent.horizontalCenter
            anchors.bottom: parent.verticalCenter
            anchors.left: parent.horizontalCenter
            anchors.topMargin: -19
            inputMask: "00000;_"
            font.pixelSize: 24
        }
    }

    Button {
        id: connectButton
        text: "Conectar"
        anchors.top: rectangle1.bottom
        anchors.topMargin: 20
        anchors.left: parent.left
        anchors.leftMargin: 50
        onClicked: connectButton.pressed = true
        onReleased: { container.serverConnect(); connectButton.pressed = false;}
    }
}
