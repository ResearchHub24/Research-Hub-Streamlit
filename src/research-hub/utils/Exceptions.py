class LoginException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class TagException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
