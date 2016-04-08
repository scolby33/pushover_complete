from urllib.parse import urljoin, parse_qs

import responses

from tests.constants import *
from tests.fixtures import PushoverAPI
from tests.util import messages_callback


@responses.activate
def test_PushoverAPI_sends_message(PushoverAPI):
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

