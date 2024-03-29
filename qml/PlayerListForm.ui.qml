import QtQuick 2.4
import Tictactoe 1.0

Item {
    id: container
    width: 400
    height: 400

    property int selectedPlayer

    Component.onCompleted: {
        container.selectedPlayer = listView.currentItem.activeFocus
    }

    ListView {
        id: listView
        x: 169
        y: 135
        width: 110
        height: 160

        model: PlayerListModel

        anchors.fill: parent
        highlight: Rectangle {
            color: "lightsteelblue"
            radius: 5
        }
        focus: true

        delegate: Item {
            x: 5
            width: parent.width
            height: 40
            Row {
                id: row1
                spacing: 10

                Text {
                    id: numberID
                    text: id
                    anchors.verticalCenter: parent.verticalCenter
                }

                Text {
                    text: name
                    font.bold: true
                    anchors.verticalCenter: parent.verticalCenter
                }

                Text {
                    text: {
                        if (gamingState == 0)
                            return "Disponível"
                        else if (gamingState == 1)
                            return "Jogando"
                        else
                            return "Ocupado"
                    }

                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            MouseArea {
                id: mouse_area1
                z: 1
                hoverEnabled: false
                anchors.fill: parent
                onClicked: {
                    listView.currentIndex = index
                    container.selectedPlayer = id
                }
            }
        }
    }
}
