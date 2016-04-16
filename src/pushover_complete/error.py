class PushoverCompleteError(Exception):
    """Root exception for pushover_complete exceptions.
    Only used to except any pushover_complete error. Will never be raised explicitly."""
    pass


class BadAPIRequestError(PushoverCompleteError):
    """An exception raised when Pushover's API responds to a request with an error."""
    pass
