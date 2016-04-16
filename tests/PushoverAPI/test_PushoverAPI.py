import re
from urllib.parse import urljoin, parse_qs

import pytest
import responses

from pushover_complete.error import BadAPIRequestError

from tests.constants import *
from tests.fixtures import *
from tests.util import *


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


@responses.activate
def test_PushoverAPI_sends_complex_message(PushoverAPI):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'messages.json'),
        callback=messages_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.send_message(
        TEST_USER,
        TEST_MESSAGE,
        device=TEST_DEVICES[0],
        title=TEST_TITLE,
        url=TEST_URL,
        url_title=TEST_URL_TITLE,
        priority=1,
        timestamp=100,
        sound='gamelan'
    )
    request_body = parse_qs(resp.request.body)
    assert request_body['token'][0] == TEST_TOKEN
    assert request_body['user'][0] == TEST_USER
    assert request_body['device'][0] == TEST_DEVICES[0]
    assert request_body['title'][0] == TEST_TITLE
    assert request_body['url'][0] == TEST_URL
    assert request_body['url_title'][0] == TEST_URL_TITLE
    assert int(request_body['priority'][0]) == 1
    assert int(request_body['timestamp'][0]) == 100
    assert request_body['sound'][0] == 'gamelan'

    assert resp.json() == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }


@responses.activate
def test_PushoverAPI_raises_error_on_bad_message(PushoverAPI):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'messages.json'),
        callback=messages_callback,
        content_type='application/json'
    )
    with pytest.raises(BadAPIRequestError):
        PushoverAPI.send_message(TEST_MESSAGE, TEST_BAD_GENERAL_ID)


@responses.activate
def test_PushoverAPI_sends_multiple_simple_messages(PushoverAPI):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'messages.json'),
        callback=messages_callback,
        content_type='application/json'
    )

    messages = [{
        'user': TEST_USER,
        'message': TEST_MESSAGE
    }] * 3
    resps = PushoverAPI.send_messages(messages)
    request_bodies = [parse_qs(resp.request.body) for resp in resps]
    assert len(resps) == 3
    assert all(request_body['token'][0] == TEST_TOKEN for request_body in request_bodies)
    assert all(request_body['user'][0] == TEST_USER for request_body in request_bodies)
    assert all(request_body['message'][0] == TEST_MESSAGE for request_body in request_bodies)
    assert all(request_body['html'][0] == 'False' for request_body in request_bodies)

    assert all(resp.json() == {
        'status': 1,
        'request': TEST_REQUEST_ID
    } for resp in resps)


@responses.activate
def test_PushoverAPI_sends_multiple_complex_messages(PushoverAPI):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'messages.json'),
        callback=messages_callback,
        content_type='application/json'
    )

    messages = [{
        'user': TEST_USER,
        'message': TEST_MESSAGE,
        'device': TEST_DEVICES[0],
        'title': TEST_TITLE,
        'url': TEST_URL,
        'url_title': TEST_URL_TITLE,
        'priority': 1,
        'timestamp': 100,
        'sound': 'gamelan'
    }] * 3
    resps = PushoverAPI.send_messages(messages)
    request_bodies = [parse_qs(resp.request.body) for resp in resps]
    assert len(resps) == 3
    assert all(request_body['token'][0] == TEST_TOKEN for request_body in request_bodies)
    assert all(request_body['user'][0] == TEST_USER for request_body in request_bodies)
    assert all(request_body['device'][0] == TEST_DEVICES[0] for request_body in request_bodies)
    assert all(request_body['title'][0] == TEST_TITLE for request_body in request_bodies)
    assert all(request_body['url'][0] == TEST_URL for request_body in request_bodies)
    assert all(request_body['url_title'][0] == TEST_URL_TITLE for request_body in request_bodies)
    assert all(int(request_body['priority'][0]) == 1 for request_body in request_bodies)
    assert all(int(request_body['timestamp'][0]) == 100 for request_body in request_bodies)
    assert all(request_body['sound'][0] == 'gamelan' for request_body in request_bodies)

    assert all(resp.json() == {
        'status': 1,
        'request': TEST_REQUEST_ID
    } for resp in resps)


@responses.activate
def test_PushoverAPI_gets_sounds(PushoverAPI):
    responses.add_callback(
        responses.GET,
        urljoin(PUSHOVER_API_URL, 'sounds.json'),
        callback=sounds_callback,
        content_type='application/json'
    )
    sounds = PushoverAPI.get_sounds()

    assert sounds == SOUNDS


@responses.activate
def test_PushoverAPI_rasies_error_on_getting_sounds_with_bad_token(BadTokenPushoverAPI):
    responses.add_callback(
        responses.GET,
        urljoin(PUSHOVER_API_URL, 'sounds.json'),
        callback=sounds_callback,
        content_type='application/json'
    )

    with pytest.raises(BadAPIRequestError):
        BadTokenPushoverAPI.get_sounds()


@responses.activate
def test_PushoverAPI_validates_user(PushoverAPI):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'users/validate.json'),
        callback=validate_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.validate(TEST_USER)

    request_body = parse_qs(resp.request.body)
    assert request_body['token'][0] == TEST_TOKEN
    assert request_body['user'][0] == TEST_USER

    assert resp.json() == {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'group': 0,
        'devices': TEST_DEVICES
    }


@responses.activate
def test_PushoverAPI_validates_group(PushoverAPI):
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'users/validate.json'),
        callback=validate_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.validate(TEST_GROUP)

    request_body = parse_qs(resp.request.body)
    assert request_body['token'][0] == TEST_TOKEN
    assert request_body['user'][0] == TEST_GROUP

    assert resp.json() == {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'group': 1,
        'devices': []
    }



@responses.activate
def test_PushoverAPI_gets_receipt(PushoverAPI):
    url_re = re.compile('https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*\.json')
    responses.add_callback(
        responses.GET,
        url_re,
        callback=receipt_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.check_receipt(TEST_RECEIPT_ID)
    request_body = parse_qs(resp.request.body)
    assert request_body['token'][0] == TEST_TOKEN
    assert resp.request.path_url.split('/')[-1].split('.')[0] == TEST_RECEIPT_ID

    assert resp.json() == {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'acknowledged': 1,
        'acknowledged_at': 100,
        'acknowledged_by': TEST_USER,
        'acknowledged_by_device': TEST_DEVICES[0],
        'last_delivered_at': 100,
        'expired': 1,
        'expires_at': 100,
        'called_back': 0,
        'called_back_at': 100
    }


@responses.activate
def test_PushoverAPI_cancels_receipt(PushoverAPI):
    url_re = re.compile('https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*/cancel\.json')
    responses.add_callback(
        responses.GET,
        url_re,
        callback=receipt_cancel_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.cancel_receipt(TEST_RECEIPT_ID)
    request_body = parse_qs(resp.request.body)
    assert request_body['token'][0] == TEST_TOKEN
    assert resp.request.path_url.split('/')[-2] == TEST_RECEIPT_ID

    assert resp.json() == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }
