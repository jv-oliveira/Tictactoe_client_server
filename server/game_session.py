from server.player import Player
from threading import Lock


class GameSession:
    def __init__(self, id: int, player_x: Player, player_o: Player):
        self._id = id
        self._choices = [None, None, None,
                         None, None, None,
                         None, None, None]
        self._playerX = player_x
        self._playerO = player_o
        self._PlayerTurn = player_x
        self._winner = None
        self._mu = Lock()

    @property
    def id(self):
        return self._id

    @property
    def choices(self):
        return self._choices

    @property
    def turn(self):
        if self._PlayerTurn is not None:
            return self._PlayerTurn.id
        else:
            return None

    def is_player_on_session(self, player_id):
        return player_id == self._playerX.id or player_id == self._playerO.id

    def make_move(self, player: Player, index: int):
        self._mu.acquire(blocking=True)
        if not self.can_make_move(index):
            ret = False
        elif player == self._playerX and player == self._PlayerTurn:
            self._choices[index] = 'X'
            self._PlayerTurn = self._playerO
            ret = True
        elif player == self._playerO and player == self._PlayerTurn:
            self._choices[index] = 'O'
            self._PlayerTurn = self._playerX
            ret = True
        else:
            ret = False
        self._mu.release()
        return ret

    def can_make_move(self, index: int):
        return index < len(self._choices) and self._choices[index] is None

    def game_finished(self):
        if self._winner is not None:
            return True
        elif len(self._choices) == 9 and self._choices.count(None) == 0:
            return True
        else:
            return False

    def choice_to_player(self, choice):
        if choice == 'X':
            return self._playerX
        elif choice == 'O':
            return self._playerO
        else:
            return None

    def winner(self) -> Player:
        for i in range(3):
            if self._choices[i] is not None:
                if self._choices[i] == self._choices[i+3] and self._choices[i] == self._choices[i+6]:
                    return self.choice_to_player(self._choices[i])
            if self._choices[i*3] is not None:
                if self._choices[i*3] == self._choices[i*3 + 1] and self._choices[i*3] == self._choices[i*3 +2]:
                    return self.choice_to_player(self._choices[i*3])

        if self._choices[0] is not None:
            if self._choices[0] == self._choices[4] and self._choices[0] == self._choices[8]:
                return self.choice_to_player(self._choices[0])
        if self._choices[2] is not None:
            if self._choices[2] == self._choices[4] and self._choices[2] == self._choices[6]:
                return self.choice_to_player(self._choices[2])
        return None