from urllib.parse import urljoin, parse_qs

import responses
import pytest

from pushover_complete.error import BadAPIRequestError

from tests.constants import *
from tests.fixtures import PushoverAPI
from tests.util import messages_callback, validate_callback


@responses.activate
def test_PushoverAPI_sends_simple_message(PushoverAPI):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'messages.json'),
        callback=messages_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.send_message(TEST_USER, TEST_MESSAGE)
    request_body = parse_qs(resp.request.body)
    assert request_body['token'][0] == TEST_TOKEN
    assert request_body['user'][0] == TEST_USER
    assert request_body['message'][0] == TEST_MESSAGE
    assert request_body['html'][0] == 'False'

    assert resp.json() == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }


def test_PushoverAPI_sends_complex_message(PushoverAPI):
    assert False

@responses.activate
def test_PushoverAPI_raises_error_on_bad_message(PushoverAPI):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'messages.json'),
        callback=messages_callback,
        content_type='application/json'
    )
    with pytest.raises(BadAPIRequestError):
        PushoverAPI.send_message(TEST_MESSAGE, TEST_BAD_USER)

@responses.activate
def test_PushoverAPI_sends_multiple_simple_messages(PushoverAPI):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'messages.json'),
        callback=messages_callback,
        content_type='application/json'
    )

    messages = [
        {
            'user': TEST_USER,
            'message': TEST_MESSAGE
        }
    ] * 3
    resps = PushoverAPI.send_messages(messages)
    request_bodies = [parse_qs(resp.request.body) for resp in resps]
    assert all(request_body['token'][0] == TEST_TOKEN for request_body in request_bodies)
    assert all(request_body['user'][0] == TEST_USER for request_body in request_bodies)
    assert all(request_body['message'][0] == TEST_MESSAGE for request_body in request_bodies)
    assert all(request_body['html'][0] == 'False' for request_body in request_bodies)

    assert all(resp.json() == {
        'status': 1,
        'request': TEST_REQUEST_ID
    } for resp in resps)


def test_PushoverAPI_sends_multiple_complex_messages(PushoverAPI):
    assert False


@responses.activate
def test_PushoverAPI_gets_sounds(PushoverAPI):
    responses.add(
        responses.GET,
        urljoin(PUSHOVER_API_URL, 'sounds.json'),
        json={'request': '287da71f5add007a511a9a019d46e371', 'status': 1, 'sounds': {'incoming': 'Incoming', 'updown': 'Up Down (long)', 'mechanical': 'Mechanical', 'spacealarm': 'Space Alarm', 'none': 'None (silent)', 'siren': 'Siren', 'gamelan': 'Gamelan', 'cashregister': 'Cash Register', 'intermission': 'Intermission', 'climb': 'Climb (long)', 'tugboat': 'Tug Boat', 'classical': 'Classical', 'alien': 'Alien Alarm (long)', 'magic': 'Magic', 'bike': 'Bike', 'persistent': 'Persistent (long)', 'bugle': 'Bugle', 'pushover': 'Pushover (default)', 'pianobar': 'Piano Bar', 'cosmic': 'Cosmic', 'falling': 'Falling', 'echo': 'Pushover Echo (long)'}}
    )
    sounds = PushoverAPI.get_sounds()

    assert sounds == {'incoming': 'Incoming', 'updown': 'Up Down (long)', 'mechanical': 'Mechanical', 'spacealarm': 'Space Alarm', 'none': 'None (silent)', 'siren': 'Siren', 'gamelan': 'Gamelan', 'cashregister': 'Cash Register', 'intermission': 'Intermission', 'climb': 'Climb (long)', 'tugboat': 'Tug Boat', 'classical': 'Classical', 'alien': 'Alien Alarm (long)', 'magic': 'Magic', 'bike': 'Bike', 'persistent': 'Persistent (long)', 'bugle': 'Bugle', 'pushover': 'Pushover (default)', 'pianobar': 'Piano Bar', 'cosmic': 'Cosmic', 'falling': 'Falling', 'echo': 'Pushover Echo (long)'}


@responses.activate
def test_PushoverAPI_validates_user(PushoverAPI):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'users/validate.json'),
        callback=validate_callback,
        content_type='application/json'
    )
    PushoverAPI.validate(TEST_USER)


# def test_PushoverAPI_gets_receipt(PushoverAPI):
#     PushoverAPI.check_receipt()
#
#
# def test_PushoverAPI_cancels_receipt(PushoverAPI):
#     PushoverAPI.cancel_receipt()
