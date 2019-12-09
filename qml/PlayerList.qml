import QtQuick 2.13
import "../qml"

Item {

    Column {
        spacing: 40
        leftPadding: 20
        bottomPadding: 20

        Row {

            id: playerIdentification
            spacing: 10

            Text {
                id: playerID
                text: "ID: " + gameManager.player_id + " |"
                font.pixelSize: 30
            }

            Text {
                id: playerName
                text: gameManager.player_name
                font.bold: true
                font.pixelSize: 30
            }
        }

        PlayerListForm {
            id: playerList

            height: 250
        }

        Row {
            spacing: 100
            Button {
                id: inviteButton
                text: "Convidar"
                onClicked: inviteButton.pressed = true
                onReleased: { gameManager.invite(playerList.selectedPlayer); inviteButton.pressed = false;}
            }

            Button {
                id: refreshButton
                text: "Atualizar"
                onClicked: refreshButton.pressed = true
                onReleased: { gameManager.playerRefresh(); refreshButton.pressed = false;}
            }
        }

    }
}
