from server.game_session import GameSession
from server.player import Player
from threading import Lock
import time


class GameSessionManager:
    def __init__(self):
        self._sessions = {}
        self._players = {}
        self._invitations = {}

        self._sessions_id_count = 0
        self._sessions_id_mu = Lock()
        self._sessions_mu = Lock()

        self._players_id_count = 0
        self._players_id_mu = Lock()
        self._players_mu = Lock()

        self._invitations_mu = Lock()

    def next_session_id(self):
        self._sessions_id_mu.acquire(blocking=True)
        self._sessions_id_count = self._sessions_id_count + 1
        id_ret = self._sessions_id_count
        self._sessions_id_mu.release()
        return id_ret

    def create_session(self, player_x: Player, player_o: Player):
        if len(self._sessions) > 32:
            return None

        self._sessions_mu.acquire(blocking=True)
        gs = GameSession(self.next_session_id(), player_x, player_o)
        self._sessions[gs.id] = gs
        self.delete_invitation(player_o)
        self.set_players_playing(player_o, player_x)
        self._sessions_mu.release()
        return gs

    def set_players_playing(self, player_o, player_x):
        self._players[player_x.id].state = Player.PLAYING
        self._players[player_o.id].state = Player.PLAYING

    def delete_invitation(self, player_o):
        self._invitations_mu.acquire(blocking=True)
        del self._invitations[player_o.id]
        self._invitations_mu.release()

    def get_session(self, session_id: int) -> GameSession:
        if session_id in self._sessions:
            return self._sessions[session_id]
        else:
            return None

    def delete_session(self, session_id: int):
        self._sessions_mu.acquire(blocking=True)
        if session_id in self._sessions:
            del self._sessions[session_id]
        self._sessions_mu.release()

    def next_player_id(self):
        self._players_id_mu.acquire(blocking=True)
        self._players_id_count = self._players_id_count + 1
        id_ret = self._players_id_count
        self._players_id_mu.release()
        return id_ret

    def create_player(self, name: str, address):
        if len(self._players) > 128:
            return None

        self._players_mu.acquire(blocking=True)
        p = Player(self.next_player_id(), name, Player.AVAILABLE, address)
        self._players[p.id] = p
        self._players_mu.release()
        return p

    def get_player(self, player_id: int) -> Player:
        if player_id in self._players:
            return self._players[player_id]
        else:
            return None

    def delete_player(self, player_id: int):
        self._players_mu.acquire(blocking=True)
        if player_id in self._players:
            del self._players[player_id]
        self._players_mu.release()

    def list_players(self):
        p = self._players.copy()
        return p

    def create_invitation(self, invitor_id, invitating_id):
        if len(self._invitations) > 32 or invitating_id in self._invitations:
            return False
        self._invitations_mu.acquire(blocking=True)
        self._invitations[invitating_id] = {'invitor': invitor_id, 'time': time.time()}
        self._invitations_mu.release()
        return True

    def check_invitation(self, player_id):
        self._invitations_mu.acquire(blocking=True)
        invite = None
        if player_id in self._invitations:
            invite = self._invitations[player_id]
        self._invitations_mu.release()
        return invite['invitor']

    def delete_invitation(self, player_id):
        self._invitations_mu.acquire(blocking=True)
        if player_id in self._invitations:
            del self._invitations[player_id]
        self._invitations_mu.release()

    def get_player_session(self, player_id):
        for session_id in self._sessions:
            session = self._sessions[session_id]
            if session.is_player_on_session(player_id):
                return session
        return None

    def remove_old_invites(self):
        invites_to_delete = []
        for i in self._invitations:
            if (time.time() - self._invitations[i]['time']) > 60*60:
                invites_to_delete.append(i)
        for i in invites_to_delete:
            self.delete_invitation(i)
