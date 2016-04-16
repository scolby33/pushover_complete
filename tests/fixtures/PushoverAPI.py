import pytest

from tests.constants import *

from pushover_complete import pushover_api


@pytest.fixture()
def PushoverAPI():
    return pushover_api.PushoverAPI(TEST_TOKEN)


@pytest.fixture()
def BadTokenPushoverAPI():
    return pushover_api.PushoverAPI(TEST_BAD_GENERAL_ID)
