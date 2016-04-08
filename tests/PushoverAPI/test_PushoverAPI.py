from tests.constants import *

from pushover_complete.pushover_api import PushoverAPI


def test_PushoverAPI_exists():
    assert isinstance(PushoverAPI(TEST_TOKEN), PushoverAPI)


def test_PushoverAPI_accepts_init_arguments():
    test_PushoverAPI = PushoverAPI(TEST_TOKEN)
    assert test_PushoverAPI.token == TEST_TOKEN
