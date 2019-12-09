from http import server, client
import json
from server.session_manager import SessionManager
from server.game_session_manager import GameSessionManager


class ServerRequestHandler(server.BaseHTTPRequestHandler):

    CONTENT_LENGTH_STR = "Content-Length"
    CONTENT_TYPE_STR = "Content-Type"
    APP_JSON_STR = "application/json"
    AUTH_STR = "Authorization"

    def __init__(self, request, client_address, s: server.ThreadingHTTPServer):
        #self._session_manager = s.sm
        #elf._game_session_manager = s.gsm
        self._session_manager = SessionManager(s.sm)
        self._game_session_manager = GameSessionManager(s.gsm)
        self._POST_map = {
            "/login": self.do_login,
            "/requestGame": self.do_request_game,
            "/invitation": self.do_invitation,
            "/gameSessionActive": self.do_game_session_active,
            "/makeMove": self.do_make_move
        }
        self._GET_map = {
            "/login": self.do_login,
            "/players": self.do_players,
            "/invitation": self.do_invitation,
            "/gameSessionActive": self.do_game_session_active,
            "/gameSessionStatus": self.do_game_session_status
        }
        super().__init__(request, client_address, s)

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

    def send_success_response(self, json_obj: dict, response_code = server.HTTPStatus.OK):
        message = json.dumps(json_obj)
        self.send_response(response_code)
        self.send_header(self.CONTENT_TYPE_STR, self.APP_JSON_STR)
        self.send_header(self.CONTENT_LENGTH_STR, len(message))
        self.end_headers()
        self.wfile.write(message.encode())

    def do_GET(self):
        # try:
            print("GET from addr: {} port: {}".format(self.client_address[0], int(self.client_address[1])))
            if self.path not in self._GET_map:
                self.send_error(server.HTTPStatus.NOT_FOUND)
            elif self.valid_headers():
                    self._GET_map[self.path]()
        # except:
        #     self.send_error(server.HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_POST(self):
        # try:
            print("POST from addr: {} port: {}".format(self.client_address[0], int(self.client_address[1])))
            if self.path not in self._POST_map:
                self.send_error(server.HTTPStatus.NOT_FOUND, "Function not found")
            elif self.path == "/login":
                print("requesting new login...")
                self.do_login()
            elif self.valid_headers():
                self._POST_map[self.path]()
        # except:
        #     self.send_error(server.HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_login(self):
        session = self.get_auth_header()
        if self.command == 'POST':
            if not self._session_manager.is_empty() and self._session_manager.check(session):
                self.send_success_response({"session": session})
            else:
                len_header = self.get_len_header()
                if len_header is None:
                    self.send_error(server.HTTPStatus.LENGTH_REQUIRED)
                else:
                    length = int(len_header)
                    player_data = json.loads(self.rfile.read(length))
                    p = self._game_session_manager.create_player(player_data['player_name'], self.client_address)
                    self.send_success_response({"session": self._session_manager.create(), "player_id": p.id})
        elif self.command == 'GET':
            self.send_success_response({"session": session})

    def do_players(self):
        players = []
        players_list = self._game_session_manager.list_players()
        for player_id in players_list:
            players.append({'id': player_id,
                            'name': players_list[player_id].name,
                            'gamingState': players_list[player_id].state})
        self.send_success_response({"players_count": len(players_list), "players": players})

    def do_make_move(self):
        move_data = self.get_json_response()
        gs = self._game_session_manager.get_session(int(move_data['game_session']))
        player = self._game_session_manager.get_player(int(move_data['player_id']))
        index = int(move_data['index_id'])
        if gs is None:
            self.send_success_response(server.HTTPStatus.NO_CONTENT)
        elif not gs.make_move(player, index):
            self.send_error(server.HTTPStatus.EXPECTATION_FAILED, "Tried to make illegal move!")
        else:
            player.address = self.client_address
            winner = gs.winner()
            self.send_success_response({
                'session': {
                    'session_id': gs.id,
                    'winner': None if winner is None else winner.name,
                    'turn': gs.turn,
                    'session_choices': gs.choices
                }
            })

    def do_game_session_status(self):
        move_data = self.get_json_response()
        gs = self._game_session_manager.get_session(int(move_data['session_id']))
        if gs is None:
            self.send_error(server.HTTPStatus.NO_CONTENT)
        else:
            winner = gs.winner()
            self.send_success_response({
                'session': {
                    'session_id': gs.id,
                    'winner': None if winner is None else winner.name,
                    'turn': gs.turn,
                    'session_choices': gs.choices
                }
            })

    def do_game_session_active(self):
        req_data = self.get_json_response()
        gs = self._game_session_manager.get_player_session(int(req_data['player_id']))
        if gs is None:
            self.send_success_response(server.HTTPStatus.NO_CONTENT)
        elif self.command == "GET":
            winner = gs.winner()
            self.send_success_response({
                'session': {
                    'session_id': gs.id,
                    'winner': None if winner is None else winner.name,
                    'turn': gs.turn,
                    'session_choices': gs.choices
                }
            })
        else:
            if bool(req_data['get_out']):
                self._game_session_manager.delete_session(gs.id)
            else:
                self.send_error(server.HTTPStatus.BAD_REQUEST)

    def get_json_response(self):
        length = int(self.get_len_header())
        move_data = json.loads(self.rfile.read(length))
        return move_data

    def do_request_game(self):
        req_data = self.get_json_response()
        invitor_id = int(req_data['invitor_id'])
        inviting_id = int(req_data['inviting_id'])
        inviting = self._game_session_manager.get_player(inviting_id)
        if inviting is None:
            self.send_error(server.HTTPStatus.BAD_REQUEST, "Player ID {} not found!".format(inviting_id))
        else:
            if self._game_session_manager.create_invitation(invitor_id, inviting_id):
                self.send_success_response({}, server.HTTPStatus.ACCEPTED)
            else:
                self.send_error(server.HTTPStatus.INTERNAL_SERVER_ERROR, "Expecting another invitation confirmation "
                                                                         "from this player")

    def do_invitation(self):
        req_data = self.get_json_response()
        player_id = int(req_data['player_id'])
        invitation_id = self._game_session_manager.check_invitation(player_id)
        invitor = self._game_session_manager.get_player(invitation_id)
        player = self._game_session_manager.get_player(player_id)
        if self.command == 'GET':
            if invitation_id is None:
                self.send_error(server.HTTPStatus.NO_CONTENT)
            else:
                self.send_success_response({
                    'invitor': {
                        'id': invitor.id,
                        'name': invitor.name
                    }
                })
        else:
            accepted = bool(req_data['accepted'])
            if accepted:
                gs = self._game_session_manager.create_session(invitor, player)
                winner = gs.winner()
                self.send_success_response({
                    'session': {
                        'session_id': gs.id,
                        'winner': None if winner is None else winner.name,
                        'turn': gs.turn,
                        'session_choices': gs.choices
                    }
                })