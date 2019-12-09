from threading import Lock

class Player:
    AVAILABLE = 0
    PLAYING = 1
    BUSY = 2

    def __init__(self, player_id: int, player_name: str, state: int, address):
        self._id = player_id
        self._name = player_name
        self._state = state
        self._state_mu = Lock()
        self._address = address

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if address is not None:
            self._address = address

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value in [self.AVAILABLE, self.PLAYING, self.BUSY]:
            self._state_mu.acquire(blocking=True)
            self._state = value
            self._state_mu.release()
