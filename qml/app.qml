import QtQuick 2.13
import QtQuick.Controls 1.4
import QtQml 2.13
import "../qml"

ApplicationWindow {
    id: window
    visible: true
    width: 500
    height: 500
    title: "Jogo da Velha"

    ServerForm {
        id: serverForm
        visible: true

        onTryConnection: {
            gameManager.tryConnection(address, port)
        }
    }

    PlayerNameForm {
        id: playerNameForm
        visible: false
    }

    CarregandoListaForm {
        id: carregandoListaForm
        visible: false
    }

    PlayerList {
        id: playersList
        visible: false
    }


    EsperandoJogadorForm {
        id: esperandoJogadorForm
        visible: false
    }

    AcceptInviteForm {
        id: acceptInviteForm
        visible: false
    }

    TicTacToe {
        id: ticTacToeGame
        visible: false
    }

    Connections {
        target: gameManager.server_comm

        onServerConnectionChanged: {
            serverForm.visible = !gameManager.server_comm.active_conn
            playerNameForm.visible = gameManager.server_comm.active_conn
            carregandoListaForm.visible = false
            playersList.visible = false
            esperandoJogadorForm.visible = false
            ticTacToeGame.visible = false
        }
    }

    Connections {
        target: gameManager

        onLoginSucceed: {
            playerNameForm.visible = false
            carregandoListaForm.visible = true
        }
    }

    Connections {
        target: gameManager

        onPlayerListReady: {
            carregandoListaForm.visible = false
            playersList.visible = true
            checkInvitesTimer.running = true
            checkInvitesTimer.restart()
        }
    }


    Connections {
        target: gameManager

        onInvite: {
            esperandoJogadorForm.visible = true
            playersList.visible = false
            checkGameTimer.running = true
            checkGameTimer.restart()
            checkInvitesTimer.running = false
            checkInvitesTimer.stop()
        }
    }

    Connections {
        target: gameManager

        onInviteArrived: {
            if (playersList.visible == false)
                return;
            acceptInviteForm.playerID = player_id
            acceptInviteForm.playerName = player_name
            acceptInviteForm.visible = true

            playersList.visible = false
            checkInvitesTimer.running = false
            checkInvitesTimer.stop()
        }
    }

    Connections {
        target: gameManager

        onGameStarted: {
            ticTacToeGame.visible = true
            esperandoJogadorForm.visible = false
            acceptInviteForm.visible = false
            checkGameTimer.running = false
            checkGameTimer.stop()
            checkGameStatusTimer.running = true
            checkGameStatusTimer.restart()
        }
    }

    Connections {
        target: gameManager

        onGameFinished: {
            ticTacToeGame.visible = false
            checkInvitesTimer.running = true
            checkInvitesTimer.restart()
            checkGameTimer.running = false
            checkGameTimer.stop()
            checkGameStatusTimer.running = false
            checkGameStatusTimer.stop()
            gameManager.playerRefresh()
            playersList.visible = true
        }
    }

    Timer {
        id: checkInvitesTimer
        interval: 1000; running: false; repeat: true
        onTriggered: gameManager.checkInvite()
    }

    Timer {
        id: checkGameStatusTimer
        interval: 500; running: false; repeat: true
        onTriggered: gameManager.checkGameStatus()
    }

    Timer {
        id: checkGameTimer
        interval: 500; running: false; repeat: true
        onTriggered: gameManager.checkActiveGame()
    }

}
