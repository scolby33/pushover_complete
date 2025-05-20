"""A Python package for interacting with *all* aspects of the Pushover API."""

from .error import BadAPIRequestError, PushoverCompleteError
from .pushover_api import PushoverAPI

__all__ = [
    "BadAPIRequestError",
    "PushoverAPI",
    "PushoverCompleteError",
]

__version__ = "2.0.0"

__license__ = "MIT License"
__copyright__ = "Copyright (c) 2025 Scott Colby"
