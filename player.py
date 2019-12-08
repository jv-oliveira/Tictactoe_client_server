class Player:
    AVAILABLE = 0
    PLAYING = 1
    BUSY = 2

    def __init__(self, player_id: int, player_name: str, state: int):
        self.player_id = player_id
        self.player_name = player_name
        self.state = state
