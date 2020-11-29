from utils.redis import RedisSession
from utils.error import NotUrlError, NotCookieError


class BaseClass:
    name = ""

    def __init__(self, chrome):
        self.chrome = chrome
        self.cookie = None

    def run(self, text):
        url = RedisSession.get_url(self.name + "_room_ls")
        if not url: raise NotUrlError(self.name)
        self.cookie = RedisSession.get_cookie(self.name + "_cookie_ls")
        if not self.cookie: raise NotCookieError(self.name)
        self.chrome.set_cookie(url, self.cookie)
        self.chrome.get_web(url, second=10)

    def is_login(self):
        return RedisSession.set_cookie(self.name + "_cookie_ls", self.cookie)
