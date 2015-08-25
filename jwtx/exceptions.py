class InvalidTokenError(Exception):
    pass


class DecodeError(InvalidTokenError):
    pass