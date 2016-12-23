"""Tests for the :mod:`pushover_complete.pushover_api.PushoverAPI` class."""

import re
try:
    from urllib.parse import urljoin, parse_qs
except ImportError:
    from urlparse import urljoin, parse_qs

import pytest
import responses

from pushover_complete.error import BadAPIRequestError

from tests.constants import *
from tests.fixtures import *
from tests.responses_callbacks import *


@responses.activate
def test_generic_get_with_payload(PushoverAPI):
    """Test the functionality of _generic_get that is missed by current uses."""
    responses.add_callback(
        responses.GET,
        urljoin(PUSHOVER_API_URL, 'foobar.json'),
        callback=generic_callback,
        content_type='application/json'
    )
    resp = PushoverAPI._generic_get('foobar.json', payload={'payload-test': 'test'})

    assert resp == {
        'status': 1,
        'payload-test': 'test'
    }


@responses.activate
def test_generic_post_without_payload(PushoverAPI):
    """Test the functionality of _generic_post that is missed by current uses."""
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'foobar.json'),
        callback=generic_callback,
        content_type='application/json'
    )
    resp = PushoverAPI._generic_post('foobar.json')

    assert resp == {
        'status': 1,
        'payload-test': False
    }

@responses.activate
def test_PushoverAPI_sends_simple_message(PushoverAPI):
    """Test the sending of a simple message."""
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'messages.json'),
        callback=messages_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.send_message(TEST_USER, TEST_MESSAGE)
    # request_body = parse_qs(resp.request.body)
    # assert request_body['token'][0] == TEST_TOKEN
    # assert request_body['user'][0] == TEST_USER
    # assert request_body['message'][0] == TEST_MESSAGE
    # assert request_body['html'][0] == 'False'

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }


@responses.activate
def test_PushoverAPI_sends_complex_message(PushoverAPI):
    """Test sending a more complex message."""
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
    # request_body = parse_qs(resp.request.body)
    # assert request_body['token'][0] == TEST_TOKEN
    # assert request_body['user'][0] == TEST_USER
    # assert request_body['device'][0] == TEST_DEVICES[0]
    # assert request_body['title'][0] == TEST_TITLE
    # assert request_body['url'][0] == TEST_URL
    # assert request_body['url_title'][0] == TEST_URL_TITLE
    # assert int(request_body['priority'][0]) == 1
    # assert int(request_body['timestamp'][0]) == 100
    # assert request_body['sound'][0] == 'gamelan'

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }


@responses.activate
def test_PushoverAPI_raises_error_on_bad_message(PushoverAPI):
    """Test proper error behavior when a malformed message is sent."""
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
    """Test sending multiple simple messages through one HTTP session."""
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
    # request_bodies = [parse_qs(resp.request.body) for resp in resps]
    # assert len(resps) == 3
    # assert all(request_body['token'][0] == TEST_TOKEN for request_body in request_bodies)
    # assert all(request_body['user'][0] == TEST_USER for request_body in request_bodies)
    # assert all(request_body['message'][0] == TEST_MESSAGE for request_body in request_bodies)
    # assert all(request_body['html'][0] == 'False' for request_body in request_bodies)

    assert all(resp == {
        'status': 1,
        'request': TEST_REQUEST_ID
    } for resp in resps)


@responses.activate
def test_PushoverAPI_sends_multiple_complex_messages(PushoverAPI):
    """Test sending multiple complex messages through one HTTP session."""
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
    # request_bodies = [parse_qs(resp.request.body) for resp in resps]
    # assert len(resps) == 3
    # assert all(request_body['token'][0] == TEST_TOKEN for request_body in request_bodies)
    # assert all(request_body['user'][0] == TEST_USER for request_body in request_bodies)
    # assert all(request_body['device'][0] == TEST_DEVICES[0] for request_body in request_bodies)
    # assert all(request_body['title'][0] == TEST_TITLE for request_body in request_bodies)
    # assert all(request_body['url'][0] == TEST_URL for request_body in request_bodies)
    # assert all(request_body['url_title'][0] == TEST_URL_TITLE for request_body in request_bodies)
    # assert all(int(request_body['priority'][0]) == 1 for request_body in request_bodies)
    # assert all(int(request_body['timestamp'][0]) == 100 for request_body in request_bodies)
    # assert all(request_body['sound'][0] == 'gamelan' for request_body in request_bodies)

    assert all(resp == {
        'status': 1,
        'request': TEST_REQUEST_ID
    } for resp in resps)


@responses.activate
def test_PushoverAPI_gets_sounds(PushoverAPI):
    """Test the retrieval of sounds."""
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
    """Test proper error behavior when a malformed request to get sounds is sent."""
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
    """Test validation of a user token."""
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'users/validate.json'),
        callback=validate_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.validate(TEST_USER)

    # request_body = parse_qs(resp.request.body)
    # assert request_body['token'][0] == TEST_TOKEN
    # assert request_body['user'][0] == TEST_USER

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'group': 0,
        'devices': TEST_DEVICES
    }


@responses.activate
def test_PushoverAPI_validates_group(PushoverAPI):
    """Test validation of a group token."""
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'users/validate.json'),
        callback=validate_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.validate(TEST_GROUP)

    # request_body = parse_qs(resp.request.body)
    # assert request_body['token'][0] == TEST_TOKEN
    # assert request_body['user'][0] == TEST_GROUP

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'group': 1,
        'devices': []
    }


@responses.activate
def test_PushoverAPI_raises_error_on_bad_user_validation(PushoverAPI):
    """Test failed validation of a token."""
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'users/validate.json'),
        callback=validate_callback,
        content_type='application/json'
    )

    with pytest.raises(BadAPIRequestError):
        PushoverAPI.validate(TEST_BAD_GENERAL_ID)


@responses.activate
def test_PushoverAPI_gets_receipt(PushoverAPI):
    """Test the retrieval of receipt details."""
    url_re = re.compile('https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*\.json')
    responses.add_callback(
        responses.GET,
        url_re,
        callback=receipt_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.check_receipt(TEST_RECEIPT_ID)
    # request_body = parse_qs(resp.request.body)
    # assert request_body['token'][0] == TEST_TOKEN
    # assert resp.request.path_url.split('/')[-1].split('.')[0] == TEST_RECEIPT_ID

    assert resp == {
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
def test_PushoverAPI_raises_error_on_bad_receipt(PushoverAPI):
    """Test the getting of a bad receipt value."""
    url_re = re.compile('https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*\.json')
    responses.add_callback(
        responses.GET,
        url_re,
        callback=receipt_callback,
        content_type='application/json'
    )
    with pytest.raises(BadAPIRequestError):
        PushoverAPI.check_receipt('r' + TEST_BAD_GENERAL_ID)  # needs to start with 'r' for the regex url match


@responses.activate
def test_PushoverAPI_cancels_receipt(PushoverAPI):
    """Test cancelling a receipt."""
    url_re = re.compile('https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*/cancel\.json')
    responses.add_callback(
        responses.POST,
        url_re,
        callback=receipt_cancel_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.cancel_receipt(TEST_RECEIPT_ID)
    # request_body = parse_qs(resp.request.body)
    # assert request_body['token'][0] == TEST_TOKEN
    # assert resp.request.path_url.split('/')[-2] == TEST_RECEIPT_ID

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }


@responses.activate
def test_PushoverAPI_raises_error_on_bad_receipt_cancel(PushoverAPI):
    """Test the cancelling of a bad receipt value."""
    url_re = re.compile('https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*/cancel\.json')
    responses.add_callback(
        responses.POST,
        url_re,
        callback=receipt_cancel_callback,
        content_type='application/json'
    )
    with pytest.raises(BadAPIRequestError):
        PushoverAPI.cancel_receipt('r' + TEST_BAD_GENERAL_ID)


@responses.activate
def test_PushoverAPI_migrates_subscription(PushoverAPI):
    """Test migrating a user key to a subscription key."""
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'subscriptions/migrate.json'),
        callback=subscription_migrate_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.migrate_to_subscription(TEST_USER, TEST_SUBSCRIPTION_CODE)
    # request_body = parse_qs(resp.request.body)
    # assert request_body['token'][0] == TEST_TOKEN
    # assert request_body['user'][0] == TEST_USER
    # assert request_body['subscription'][0] == TEST_SUBSCRIPTION_CODE

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'subscribed_user_key': TEST_SUBSCRIBED_USER_KEY
    }


@responses.activate
def test_PushoverAPI_raises_error_on_subscription_migration_with_bad_user(PushoverAPI):
    """Test a migration of a bad user key."""
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'subscriptions/migrate.json'),
        callback=subscription_migrate_callback,
        content_type='application/json'
    )
    with pytest.raises(BadAPIRequestError):
        PushoverAPI.migrate_to_subscription(TEST_BAD_GENERAL_ID, TEST_SUBSCRIPTION_CODE)


@responses.activate
def test_PushoverAPI_migrates_multiple_subscriptions(PushoverAPI):
    """Test a migration of multiple user keys at once."""
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'subscriptions/migrate.json'),
        callback=subscription_migrate_callback,
        content_type='application/json'
    )
    users = [{
        'user': TEST_USER
    }] * 3
    resps = PushoverAPI.migrate_multiple_to_subscription(users, TEST_SUBSCRIPTION_CODE)
    # request_bodies = [parse_qs(resp.request.body) for resp in resps]
    # assert len(resps) == 3
    # assert all(request_body['token'][0] == TEST_TOKEN for request_body in request_bodies)
    # assert all(request_body['user'][0] == TEST_USER for request_body in request_bodies)
    # assert all(request_body['subscription'][0] == TEST_SUBSCRIPTION_CODE for request_body in request_bodies)

    assert all(resp == {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'subscribed_user_key': TEST_SUBSCRIBED_USER_KEY
    } for resp in resps)


@responses.activate
def test_PushoverAPI_gets_group_info(PushoverAPI):
    """Test getting group info"""
    url_re = re.compile('https://api\.pushover\.net/1/groups/g[a-zA-Z0-9]*\.json')
    responses.add_callback(
        responses.GET,
        url_re,
        callback=groups_callback,
        content_type='application/json'
    )

    resp = PushoverAPI.group_info(TEST_GROUP)
    # request_body = parse_qs(resp.request.body)
    # assert request_body['token'][0] == TEST_TOKEN
    # assert resp.request.path_url.split('/')[-1].split('.')[0] == TEST_GROUP

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'name': TEST_GROUP_NAME,
        'users': [
            {
                'user': TEST_USER,
                'device': TEST_DEVICES[0],
                'memo': '',
                'disabled': False
            },
            {
                'user': TEST_USER,
                'device': TEST_DEVICES[1],
                'memo': '',
                'disabled': False
            }
        ]
    }


@responses.activate
def test_PushoverAPI_adds_user_to_group(PushoverAPI):
    """Test adding a user to a group"""
    url_re = re.compile('https://api\.pushover\.net/1/groups/g[a-zA-Z0-9]*/add_user\.json')
    responses.add_callback(
        responses.POST,
        url_re,
        callback=groups_add_user_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.group_add_user(TEST_GROUP, TEST_USER)

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }


@responses.activate
def test_PushoverAPI_deletes_user_from_group(PushoverAPI):
    """Test removing a user from a group"""
    url_re = re.compile('https://api\.pushover\.net/1/groups/g[a-zA-Z0-9]*/delete_user\.json')
    responses.add_callback(
        responses.POST,
        url_re,
        callback=groups_delete_user_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.group_delete_user(TEST_GROUP, TEST_USER)

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }


@responses.activate
def test_PushoverAPI_disables_user_in_group(PushoverAPI):
    """Test disabling a user in a group."""
    url_re = re.compile('https://api\.pushover\.net/1/groups/g[a-zA-Z0-9]*/disable_user\.json')
    responses.add_callback(
        responses.POST,
        url_re,
        callback=groups_disable_user_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.group_disable_user(TEST_GROUP, TEST_USER)

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }


@responses.activate
def test_PushoverAPI_enables_user_in_group(PushoverAPI):
    """Test enabling a user in a group."""
    url_re = re.compile('https://api\.pushover\.net/1/groups/g[a-zA-Z0-9]*/enable_user\.json')
    responses.add_callback(
        responses.POST,
        url_re,
        callback=groups_enable_user_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.group_enable_user(TEST_GROUP, TEST_USER)

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }


@responses.activate
def test_PushoverAPI_changes_group_name(PushoverAPI):
    """Test changing group name."""
    url_re = re.compile('https://api\.pushover\.net/1/groups/g[a-zA-Z0-9]*/rename\.json')
    responses.add_callback(
        responses.POST,
        url_re,
        callback=groups_rename_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.group_rename(TEST_GROUP, TEST_GROUP_NAME + 'New')

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID
    }


@responses.activate
def test_PushoverAPI_assigns_license_to_user(PushoverAPI):
    """Test assigning a license to a user."""
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'licenses/assign.json'),
        callback=licenses_assign_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.assign_license(TEST_USER)

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'credits': 0
    }


@responses.activate
def test_PushoverAPI_assigns_license_to_email(PushoverAPI):
    """Test assigning a license to an email."""
    responses.add_callback(
        responses.POST,
        urljoin(PUSHOVER_API_URL, 'licenses/assign.json'),
        callback=licenses_assign_callback,
        content_type='application/json'
    )
    resp = PushoverAPI.assign_license(TEST_USER_EMAIL)

    assert resp == {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'credits': 0
    }
