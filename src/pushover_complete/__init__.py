"""A Python package for interacting with *all* aspects of the Pushover API"""

from .error import PushoverCompleteError, BadAPIRequestError
from .pushover_api import PushoverAPI

__all__ = [
    "PushoverCompleteError",
    "BadAPIRequestError",
    "PushoverAPI",
]

__version__ = "1.1.2-dev"

__license__ = "MIT License"
__copyright__ = "Copyright (c) 2024 Scott Colby"
