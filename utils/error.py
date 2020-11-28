class BaseError(Exception):
    pass


class NotCookieError(BaseError):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "NotCookieError name: {} ".format(self.name)


class NotUrlError(BaseError):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "NotUrlError name: {} ".format(self.name)
