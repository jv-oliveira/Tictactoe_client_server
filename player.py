from enum import Enum


class State(Enum):
    AVAILABLE = 1
    PLAYING = 2
    BUSY = 3


class Player:
    def __init__(self, player_id: int, player_name: str, state: State):
        self.player_id = player_id
        self.player_name = player_name
        self.state = state
