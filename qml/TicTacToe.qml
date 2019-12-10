/****************************************************************************
**
** Copyright (C) 2015 The Qt Company Ltd.
** Contact: http://www.qt.io/licensing/
**
** This file is part of the examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

/**
    Baseado no exemplo dado em https://doc.qt.io/archives/qt-4.8/qt-declarative-toys-tic-tac-toe-qml-tic-tac-toe-tic-tac-toe-qml.html
**/
import QtQuick 2.13
import QtQuick.Controls 1.4
import "../qml/"

Rectangle {

    id: game
    property bool running: true
    property int playerIndex: 0

    width: display.width; height: display.height + 10

    Text {
        id: textMsg
        text: {
            if (gameManager.winner !== undefined && gameManager.winner !== "") {
                return gameManager.winner + " venceu!";
            } else if (!gameManager.board_str.includes(' ')) {
                return "Empate!";
            } else if (gameManager.turn == gameManager.player_id) {
                return "Sua vez";
            } else {
                return "Vez do adversário";
            }
        }

        font.family: "Helvetica"
        font.pointSize: 24
        anchors.top: parent.top
    }

    Image {
        id: boardImage
        anchors.top: textMsg.bottom
        source: applicationDirPath + "/images/board.png"
    }

    Column {
        id: display
        anchors.top: boardImage.top
        Grid {
            id: board
            width: boardImage.width; height: boardImage.height
            columns: 3

            Repeater {
                model: 9

                OXBox {
                    width: board.width/3
                    height: board.height/3
                    state: gameManager.board_str[index]

                    onClicked: {
                        if (gameManager.winner === undefined || gameManager.winner === "") {
                            if (gameManager.turn == gameManager.player_id) {
                                console.log(gameManager.board_str[index]);
                                console.log(gameManager.board_str);
                                gameManager.makeMove(index);
                            }
                        }
                    }
                }
            }
        }
    }

    Button {
        id: backButton
        text: "Voltar"
        anchors.right: boardImage.right
        anchors.top: boardImage.bottom
        anchors.margins: 20
        onClicked: backButton.pressed = true
        onReleased: { gameManager.gameFinished(); backButton.pressed = false;}
    }
}
