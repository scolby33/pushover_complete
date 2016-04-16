import pytest

from tests.constants import *

from pushover_complete import pushover_api


@pytest.fixture()
def PushoverAPI():
    """A fixture for the :class:`pushover_complete.pushover_api.PushoverAPI` class, properly instantiated with a "good" application token."""
    return pushover_api.PushoverAPI(TEST_TOKEN)


@pytest.fixture()
def BadTokenPushoverAPI():
    """A fixture for :class:`pushover_complete.pushover_api.PushoverAPI`, instantiated with a "bad" application token."""
    return pushover_api.PushoverAPI(TEST_BAD_GENERAL_ID)
