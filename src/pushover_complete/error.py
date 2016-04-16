class PushoverCompleteError(Exception):
    pass


class BadAPIRequestError(PushoverCompleteError):
    pass
