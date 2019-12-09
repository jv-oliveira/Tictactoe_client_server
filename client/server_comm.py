import http.client
from http.server import HTTPStatus
import json
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot


class ServerComm(QObject):
    CONTENT_LENGTH_STR = "Content-Length"
    CONTENT_TYPE_STR = "Content-Type"
    APP_JSON_STR = "application/json"
    AUTH_STR = "Authorization"

    serverConnectionChanged = pyqtSignal()

    def __init__(self, parent: QObject):
        super().__init__(parent)
        self._server_conn = None
        self._auth = None

    @pyqtSlot(str, int)
    def connect_to_server(self, host: str, port: int):
        print("Trying to connect to server {}:{}".format(host, port))
        self._server_conn = http.client.HTTPConnection(host, port, timeout=10)
        # if self._server_conn.sock is None:
        #     print('Not Connected!')
        # else:
        #     print('Connected!')
        self.serverConnectionChanged.emit()

    @pyqtProperty('bool')
    def active_conn(self) -> bool:
        return True
        # return self._server_conn.sock is not None

    def _get_default_header(self, content_length: int):
        return {self.CONTENT_TYPE_STR: self.APP_JSON_STR,
                self.AUTH_STR: self._auth,
                self.CONTENT_LENGTH_STR: content_length}

    def empty_response(self, response_bytes) -> bool:
        return response_bytes == b"" or response_bytes is None or len(response_bytes) == 0

    def _request_and_response(self, command: str, endpoint: str, json_msg: dict = None) -> [int, dict]:
        msg = None if json_msg is None else json.dumps(json_msg)
        headers = self._get_default_header(len(msg) if msg is not None else 0)
        self._server_conn.request(command, endpoint, msg, headers)
        response = self._server_conn.getresponse()
        response_bytes = response.read()
        # print(b"BYTES: " + response_bytes)
        response_json = None if self.empty_response(response_bytes) else json.loads(response_bytes.decode())
        return response.code, response_json

    def get_new_login(self, name: str) -> int:
        msg_body = {"player_name": name}
        json_msg = json.dumps(msg_body)
        headers = {self.CONTENT_TYPE_STR: self.APP_JSON_STR,
                   self.CONTENT_LENGTH_STR: len(json_msg)}
        self._server_conn.request('POST', '/login', json_msg, headers)
        response = self._server_conn.getresponse()
        if response.code != HTTPStatus.OK:
            print("Fail to get login")
            return None
        else:
            json_response = json.loads(response.read().decode())
            self._auth = json_response["session"]
            player_id = json_response["player_id"]
            return player_id

    def get_players(self) -> dict:
        code, response = self._request_and_response('GET', '/players')
        if code != HTTPStatus.OK:
            print("Falha ao pegar jogadores ativos")
            return None
        else:
            if int(response["players_count"]) > 0:
                return response["players"]
            else:
                return None

    def request_game(self, player_id, invite_id) -> bool:
        code, response = self._request_and_response('POST', '/requestGame', {
            "invitor_id": player_id,
            "inviting_id": invite_id
        })
        return code != HTTPStatus.OK

    def check_invitation(self, player_id: int) -> [int, str]:
        code, response = self._request_and_response('GET', '/invitation', {
            "player_id": player_id
        })
        if code != HTTPStatus.OK:
            return None, None
        else:
            return int(response["invitor"]['id']), response["invitor"]['name']

    def check_active_session(self, player_id: int) -> dict:
        code, response = self._request_and_response('GET', '/gameSessionActive', {
            "player_id": player_id
        })
        if code != HTTPStatus.OK or response is None:
            return None
        else:
            print(type(response))
            print(response)
            return response["session"]

    def quit_session(self, player_id: int) -> dict:
        code, response = self._request_and_response('POST', '/gameSessionActive', {
            "player_id": player_id,
            "quit": True
        })
        if code != HTTPStatus.OK or response is None:
            return None
        else:
            return response["session"]

    def check_session_status(self, session_id: int) -> dict:
        code, response = self._request_and_response('GET', '/gameSessionStatus', {
            "session_id": session_id
        })
        if code != HTTPStatus.OK or response is None:
            return None
        else:
            return response["session"]

    def answer_invitation(self, player_id: int, accept: bool) -> dict:
        code, response = self._request_and_response('POST', '/invitation', {
            "player_id": player_id,
            "accepted": accept
        })
        if code != HTTPStatus.OK:
            return None
        else:
            return response["session"]

    def make_move(self, session_id: int, player_id: int, board_index: int) -> dict:
        code, response = self._request_and_response('POST', '/makeMove', {
            "game_session": session_id,
            "player_id": player_id,
            "index_id": board_index
        })
        if code != HTTPStatus.OK or response is None:
            return None
        else:
            return response["session"]
