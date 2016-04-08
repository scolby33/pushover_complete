import pytest

from tests.constants import *

from pushover_complete.pushover_api import PushoverAPI


@pytest.fixture()
def PushoverAPI():
    return PushoverAPI(TEST_TOKEN)
