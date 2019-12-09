from http import server, client
import json
from server.session_manager import SessionManager
from server.game_session_manager import GameSessionManager


class ServerRequestHandler(server.BaseHTTPRequestHandler):

    CONTENT_LENGTH_STR = "Content-Length"
    CONTENT_TYPE_STR = "Content-Type"
    APP_JSON_STR = "application/json"
    AUTH_STR = "Authorization"

    def __init__(self, request, client_address, server: server.ThreadingHTTPServer):
        self._session_manager = server.sm
        self._game_session_manager = server.gsm
        self._POST_map = {
            "/login": self.do_login,
            "/requestGame": self.do_request_game,
            "/makeMove": self.do_make_move
        }
        self._GET_map = {
            "/login": self.do_login,
            "/players": self.do_players,
            "/gameSessionStatus": self.do_game_session
        }
        super().__init__(request, client_address, server)

    def get_auth_header(self):
        return self.headers[self.AUTH_STR]

    def get_type_header(self):
        return self.headers[self.CONTENT_TYPE_STR]

    def get_len_header(self):
        return self.headers[self.CONTENT_LENGTH_STR]

    def valid_headers(self):
        if not self._session_manager.check(self.get_auth_header()):
            self.send_error(server.HTTPStatus.UNAUTHORIZED)
        elif self.get_type_header() != self.APP_JSON_STR:
            self.send_error(server.HTTPStatus.BAD_REQUEST, self.CONTENT_TYPE_STR + ' is not ' + self.APP_JSON_STR)
        elif self.get_len_header() is None:
            self.send_error(server.HTTPStatus.LENGTH_REQUIRED)
        else:
            return True
        return False

    def send_ok_response(self, json_obj: dict):
        message = json.dumps(json_obj)
        self.send_response(server.HTTPStatus.OK)
        self.send_header(self.CONTENT_TYPE_STR, self.APP_JSON_STR)
        self.send_header(self.CONTENT_LENGTH_STR, len(message))
        self.end_headers()
        self.wfile.write(message.encode())

    def do_GET(self):
        print("GET from addr: {} port: {}".format(self.client_address[0], int(self.client_address[1])))
        if self.path not in self._GET_map:
            self.send_error(server.HTTPStatus.NOT_FOUND)
        elif self.valid_headers():
                self._GET_map[self.path]()

    def do_POST(self):
        print("POST from addr: {} port: {}".format(self.client_address[0], int(self.client_address[1])))
        if self.path not in self._POST_map:
            self.send_error(server.HTTPStatus.NOT_FOUND, "Function not found")
        elif self.path == "/login":
            print("requesting new login...")
            self.do_login()
        elif self.valid_headers():
            self._POST_map[self.path]()

    def do_login(self):
        session = self.get_auth_header()
        if self.command == 'POST':
            if not self._session_manager.is_empty() and self._session_manager.check(session):
                self.send_ok_response({"session": session})
            else:
                len_header = self.get_len_header()
                if len_header is None:
                    self.send_error(server.HTTPStatus.LENGTH_REQUIRED)
                else:
                    length = int(len_header)
                    player_data = json.loads(self.rfile.read(length))
                    p = self._game_session_manager.create_player(player_data['player_name'], self.client_address)
                    self.send_ok_response({"session": self._session_manager.create(), "player_id": p.id})
        elif self.command == 'GET':
            self.send_ok_response({"session": session})

    def do_players(self):
        players = []
        players_list = self._game_session_manager.list_players()
        for player_id in players_list:
            players.append({'id': player_id,
                            'name': players_list[player_id].name,
                            'gamingState': players_list[player_id].state})
        self.send_ok_response({"players_count": len(players_list), "players": players})

    def do_make_move(self):
        length = int(self.get_len_header())
        move_data = json.loads(self.rfile.read(length))
        gs = self._game_session_manager.get_session(int(move_data['game_session']))
        player = self._game_session_manager.get_player(int(move_data['player_id']))
        index = int(move_data['player_id'])
        if gs is None:
            self.send_ok_response(server.HTTPStatus.NO_CONTENT)
        elif not gs.make_move(player, index):
            self.send_error(server.HTTPStatus.EXPECTATION_FAILED, "Tried to make illegal move!")
        else:
            player.address = self.client_address
            self.send_ok_response({
                'session': {
                    'session_id': gs.id,
                    'winner': gs.winner().id,
                    'turn': gs.turn.id,
                    'session_choices': gs.choices
                }
            })

    def do_game_session(self):
        length = int(self.get_len_header())
        move_data = json.loads(self.rfile.read(length))
        gs = self._game_session_manager.get_session(int(move_data['game_session']))
        if gs is None:
            self.send_ok_response(server.HTTPStatus.NO_CONTENT)
        else:
            self.send_ok_response({
                'session': {
                    'session_id': gs.id,
                    'winner': gs.winner().id,
                    'turn': gs.turn.id,
                    'session_choices': gs.choices
                }
            })

    def do_request_game(self):
        length = int(self.get_len_header())
        req_data = json.loads(self.rfile.read(length))
        invitor_id = int(req_data['invitor_id'])
        inviting_id = int(req_data['inviting_id'])
        invitor = self._game_session_manager.get_player(invitor_id)
        inviting = self._game_session_manager.get_player(inviting_id)
        if inviting is None:
            self.send_error(server.HTTPStatus.BAD_REQUEST, "Player ID {} not found!".format(inviting_id))
        else:
            response = self.request_player_invitation(inviting, invitor)
            if response is None:
                self.send_error(server.HTTPStatus.REQUEST_TIMEOUT)
            else:
                response_json = self.process_player_invitation_response(inviting, invitor, response)
                self.send_ok_response(response_json)

    def process_player_invitation_response(self, inviting, invitor, response):
        accepted = True
        gs = None
        if response.getcode() != server.HTTPStatus.ACCEPTED:
            accepted = False
        else:
            gs = self._game_session_manager.create_session(invitor, inviting)
        response_json = {'accepted': accepted, 'session': None}
        if gs is not None:
            response_json['session'] = {
                'session_id': gs.id,
                'winner': gs.winner().id,
                'turn': gs.turn.id,
                'session_choices': gs.choices
            }
        return response_json

    def request_player_invitation(self, inviting, invitor):
        message = json.dumps({'invitor': {'id': invitor.id, 'name': invitor.name}})
        conn = client.HTTPSConnection(inviting.address[0], inviting.address[1], timeout=10)
        headers = {self.CONTENT_TYPE_STR: self.APP_JSON_STR, self.CONTENT_LENGTH_STR: len(message)}
        conn.request('POST', '/invite', message, headers)
        response = conn.getresponse()
        return response













