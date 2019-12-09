from PyQt5.QtCore import pyqtProperty, QObject, pyqtSignal, pyqtSlot, QAbstractListModel
from client.server_comm import ServerComm
from client.PlayerListModel import PlayerListModel


class LocalGameManager(QObject):
    CROSS = 'X'
    CIRCLE = 'O'

    # signals
    boardChanged = pyqtSignal()
    winnerChanged = pyqtSignal()
    playerNameChanged = pyqtSignal()
    markBoard = pyqtSignal()
    invite = pyqtSignal(int)
    checkInvite = pyqtSignal()
    inviteArrived = pyqtSignal(int, str, arguments=['player_id', 'player_name'])
    inviteChanged = pyqtSignal(bool)
    acceptInvite = pyqtSignal(bool, arguments=['accept'])
    tryLogin = pyqtSignal(str)
    loginSucceed = pyqtSignal()
    serverCommChanged = pyqtSignal()
    tryConnection = pyqtSignal(str, int)
    playerListReady = pyqtSignal()
    playerRefresh = pyqtSignal()
    playerListModelChanged = pyqtSignal()
    playerIdChanged = pyqtSignal()
    gameStarted = pyqtSignal()
    checkGameStatus = pyqtSignal()
    checkActiveGame = pyqtSignal()
    gameFinished = pyqtSignal()
    turnChanged = pyqtSignal()
    makeMove = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self._player_symbol = None
        self._player_name = None
        self._player_id = None
        self._session_id = None
        self._winner = None
        self._turn = None
        self._running = False
        self._board = [None, None, None,
                       None, None, None,
                       None, None, None]
        self._board_str = LocalGameManager.board_to_str(self._board)
        self._server_comm = ServerComm(self)
        self._player_list_model = PlayerListModel()
        self._login_accept = False
        self.invite.connect(self.invite_handler)
        self.tryConnection.connect(self._server_comm.connect_to_server)
        self.tryLogin.connect(self.try_login)
        self.loginSucceed.connect(self.update_players_list)
        self.playerRefresh.connect(self.update_players_list)
        self.checkInvite.connect(self.check_invite)
        self.acceptInvite.connect(self.accept_invite)
        self.checkGameStatus.connect(self.check_game_status)
        self.checkActiveGame.connect(self.check_active_game)
        self.makeMove.connect(self.make_move)


    @pyqtProperty(str)
    def player_symbol(self):
        return self._player_symbol

    @pyqtProperty(str)
    def invite_accept(self):
        return self._invite_accept

    @pyqtProperty(ServerComm, notify=serverCommChanged)
    def server_comm(self):
        return self._server_comm

    @pyqtProperty(PlayerListModel, notify=playerListModelChanged)
    def player_list_model(self):
        return self._player_list_model

    @player_symbol.setter
    def player_symbol(self, player_symbol: str):
        if player_symbol in ['X', 'O']:
            self._player_symbol = player_symbol

    @pyqtProperty(str, notify=playerNameChanged)
    def player_name(self):
        return self._player_name

    @pyqtProperty(int, notify=turnChanged)
    def turn(self):
        return self._turn if self._turn is not None else -1

    @player_name.setter
    def player_name(self, player_name: str):
        prev = self._player_name
        self._player_name = player_name
        if prev != player_name:
            self.playerNameChanged.emit()

    @pyqtProperty(int, notify=playerIdChanged)
    def player_id(self):
        if self._player_id is None:
            return 0
        else:
            return int(self._player_id)

    @player_id.setter
    def player_id(self, player_id: int):
        self._player_id = player_id

    @pyqtProperty(str, notify=boardChanged)
    def board_str(self):
        return self._board_str

    @staticmethod
    def board_to_str(board):
        ret = ""
        for i in board:
            if i == 'X' or i == 'O':
                ret += i
            else:
                ret += " "
        return ret

    @pyqtSlot(int)
    def invite_handler(self, invite_id: int):
        if not self._server_comm.request_game(self._player_id, invite_id):
            self.inviteFailed.emit()

    @pyqtSlot(str)
    def try_login(self, player_name: str):
        self._player_name = player_name
        self.playerNameChanged.emit()
        self._player_id = self._server_comm.get_new_login(player_name)
        if self._player_id is not None:
            self.loginSucceed.emit()
            self.playerIdChanged.emit()

    @pyqtSlot()
    def check_invite(self):
        id, name = self._server_comm.check_invitation(self._player_id)
        if id is not None and name is not None:
            self.inviteArrived.emit(id, name)

    @pyqtSlot(bool)
    def accept_invite(self, accept: bool):
        session = self._server_comm.answer_invitation(self._player_id, accept)
        if accept and session is not None:
            self.clear_for_new_game()
            self._session_id = session['session_id']
            self._winner = session['winner']
            self._turn = session['turn']
            self.update_board(session['session_choices'])
            self.turnChanged.emit()
            self.gameStarted.emit()
        else:
            self.gameFinished.emit()

    @pyqtSlot()
    def check_game_status(self):
        session = self._server_comm.check_session_status(self._session_id)
        if session is None:
            self.gameFinished.emit()
            self.clear_for_new_game()
            return
        self._session_id = session['session_id']
        self.update_winner(session['winner'])
        self._turn = session['turn']
        self.update_board(session['session_choices'])
        self.turnChanged.emit()
        self.gameStarted.emit()

    @pyqtSlot()
    def check_active_game(self):
        session = self._server_comm.check_active_session(self._player_id)
        if session is None:
            print("Still no session!")
            return
        print("Let's go!")
        self.clear_for_new_game()
        self._session_id = session['session_id']
        self.update_winner(session['winner'])
        self._turn = session['turn']
        self._board = session['session_choices']
        self.boardChanged.emit()
        self.turnChanged.emit()
        self.gameStarted.emit()

    @pyqtSlot(int)
    def make_move(self, index):
        session = self._server_comm.make_move(self._session_id, self._player_id, index)
        if session is None:
            print("Still no session!")
            return
        print("Let's go!")
        self.clear_for_new_game()
        self._session_id = session['session_id']
        self.update_winner(session['winner'])
        self._turn = session['turn']
        self.update_board(session['session_choices'])
        self.turnChanged.emit()

    @property
    def board(self):
        return self._board

    def set_up_server_comm(self, server_comm: ServerComm):
        if server_comm is not None:
            self._server_comm = server_comm

    def update_board(self, board):
        prev = self._board
        self._board = board
        self._board_str = LocalGameManager.board_to_str(board)
        if prev != board:
            self.boardChanged.emit()

    def update_winner(self, winner: str):
        prev = self._winner
        self._winner = winner
        if prev != winner:
            self.winnerChanged.emit()

    def clear_for_new_game(self):
        self.update_board([None, None, None,
                           None, None, None,
                           None, None, None])
        self._player_symbol = None
        self._session_id = None
        self._winner = None

    @pyqtSlot()
    def update_players_list(self):
        players = self._server_comm.get_players()
        for i in range(len(players)):
            if players[i]['id'] == self._player_id:
                del players[i]
                break
        self._player_list_model.update_players(players)
        self.playerListReady.emit()
        self.playerListModelChanged.emit()


