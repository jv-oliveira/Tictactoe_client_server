from random import seed, choice
import time


class SessionManager:
    valid_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def __init__(self, key_timeout: int = 60*60):
        self._keylist = {}
        self._key_timeout = key_timeout

    def random_char(self):
        return choice(self.valid_chars)

    def gen_cookie_key(self, length: int = 32) -> str:
        seed(time.localtime())
        cookie_key = ""
        for i in range(0, length):
            cookie_key += self.random_char()
        return cookie_key

    def check(self, key: str):
        if key in self._keylist:
            elapsed = time.time() - self._keylist[key]
            if self._key_timeout < elapsed:
                del self._key_timeout[key]
            else:
                return True
        return False

    def create(self) -> str:
        key = self.gen_cookie_key()
        while self.check(key):
            key = self.gen_cookie_key()
        self._keylist[key] = time.time()
        return key

    def remove(self, key: str):
        if key in self._keylist:
            del self._keylist[key]
            return True
        else:
            return

    def is_empty(self):
        return len(self._keylist) == 0
