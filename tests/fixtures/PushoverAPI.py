"""Fixtures used for testing pushover_complete."""  # noqa: N999 -- weird name for fixture module is okay

import pytest

from pushover_complete import pushover_api
from tests.constants import TEST_BAD_GENERAL_ID, TEST_TOKEN


@pytest.fixture
def PushoverAPI():
    """Fixture for :class:`pushover_complete.pushover_api.PushoverAPI`, instantiated with a "good" application token."""
    return pushover_api.PushoverAPI(TEST_TOKEN)


@pytest.fixture
def BadTokenPushoverAPI():
    """Fixture for :class:`pushover_complete.pushover_api.PushoverAPI`, instantiated with a "bad" application token."""
    return pushover_api.PushoverAPI(TEST_BAD_GENERAL_ID)
