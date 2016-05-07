"""Callbacks used by the :mod:`responses` module for mocking out API requests."""

import json
from urllib.parse import parse_qs

from tests.constants import *


def messages_callback(request):
    """A callback to mock the `/messages.json` endpoint."""
    resp_body = {
        'request': TEST_REQUEST_ID
    }
    headers = {'X-Request-Id': TEST_REQUEST_ID}

    req_body = getattr(request, 'body', None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get('message', None) is None:
        resp_body['message'] = 'cannot be blank'
        resp_body['status'] = 0
        resp_body['errors'] = ['message cannot be blank']
    elif qs.get('token', None) != TEST_TOKEN:
        resp_body['token'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['application token is invalid']
    elif qs.get('user', None) != TEST_USER and qs.get('user', None) != TEST_GROUP:  # allow TEST_USER or TEST_GROUP
        resp_body['user'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['user identifier is not a valid user, group, or subscribed user key']
    elif qs.get('priority', None) == 2:
        if qs.get('expire', None) is None:
            resp_body['expire'] = 'must be supplied with priority=2'
            resp_body['status'] = 0
            resp_body['errors'] = ['expire must be supplied with priority=2']
        elif qs.get('retry', None) is None:
            resp_body['retry'] = 'must be supplied with priority=2'
            resp_body['status'] = 0
            resp_body['errors'] = ['retry must be supplied with priority=2']
        else:
            resp_body['receipt'] = TEST_RECEIPT_ID
    else:
        resp_body['status'] = 1

    return 200 if resp_body['status'] == 1 else 400, headers, json.dumps(resp_body)


def sounds_callback(request):
    """A callback to mock the `/sounds.json` endpoint."""
    resp_body = {
        'request': TEST_REQUEST_ID
    }
    headers = {'X-Request-Id': TEST_REQUEST_ID}

    req_body = getattr(request, 'body', None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get('token', None) != TEST_TOKEN:
        resp_body['token'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['application token is invalid']
    else:
        resp_body['status'] = 1
        resp_body['sounds'] = SOUNDS

    return 200 if resp_body['status'] == 1 else 400, headers, json.dumps(resp_body)


def validate_callback(request):
    """A callback to mock the `/users/validate.json` endpoint."""
    resp_body = {
        'request': TEST_REQUEST_ID
    }
    headers = {'X-Request-Id': TEST_REQUEST_ID}

    req_body = getattr(request, 'body', None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get('token', None) != TEST_TOKEN:
        resp_body['token'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['application token is invalid']

    user = qs.get('user', None)
    if user == TEST_USER:
        device = qs.get('device', None)
        if device and device.lower() not in TEST_DEVICES:
            resp_body['device'] = 'invalid for this user'
            resp_body['status'] = 0
            resp_body['errors'] = ['device name is not valid for this user']
        else:
            resp_body['status'] = 1
            resp_body['group'] = 0
            resp_body['devices'] = TEST_DEVICES
    elif user == TEST_GROUP:
        resp_body['status'] = 1
        resp_body['group'] = 1
        resp_body['devices'] = []
    else:
        resp_body['user'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['user identifier is not a valid user, group, or subscribed user key']

    return 200 if resp_body['status'] == 1 else 400, headers, json.dumps(resp_body)


def receipt_callback(request):
    """A callback to mock the /receipts/{receipt}.json endpoint.

    Best used like so::

        url_re = re.compile('https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*\.json')
        responses.add_callback(
            responses.GET,
            url_re,
            callback=receipt_callback,
            content_type='application/json'
        )

    in order to capture all calls to the endpoint.
    """
    resp_body = {
        'request': TEST_REQUEST_ID
    }
    headers = {'X-Request-Id': TEST_REQUEST_ID}

    req_body = getattr(request, 'body', None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get('token', None) != TEST_TOKEN:
        resp_body['token'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['application token is invalid']
    elif request.path_url.split('/')[-1].split('.')[0] != TEST_RECEIPT_ID:  # get the receipt from a url of the form /1/receipts/{receipt}.json
        resp_body['receipt'] = 'not found'
        resp_body['status'] = 0
        resp_body['errors'] = ['receipt not found; may be invalid or expired']
    else:
        resp_body['status'] = 1
        resp_body['acknowledged'] = 1
        resp_body['acknowledged_at'] = 100
        resp_body['acknowledged_by'] = TEST_USER
        resp_body['acknowledged_by_device'] = TEST_DEVICES[0]
        resp_body['last_delivered_at'] = 100
        resp_body['expired'] = 1
        resp_body['expires_at'] = 100
        resp_body['called_back'] = 0
        resp_body['called_back_at'] = 100

    return 200 if resp_body['status'] == 1 else 400, headers, json.dumps(resp_body)


def receipt_cancel_callback(request):
    """A callback to mock the /receipts/{receipt}/cancel.json endpoint.

    Best used like so::

            url_re = re.compile('https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*/cancel\.json')
        responses.add_callback(
            responses.GET,
            url_re,
            callback=receipt_cancel_callback,
            content_type='application/json'
        )

    in order to capture all calls to the endpoint.
    """
    resp_body = {
        'request': TEST_REQUEST_ID
    }
    headers = {'X-Request-Id': TEST_REQUEST_ID}

    req_body = getattr(request, 'body', None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get('token', None) != TEST_TOKEN:
        resp_body['token'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['application token is invalid']
    elif request.path_url.split('/')[-2] != TEST_RECEIPT_ID:  # get the receipt from a url of the form /1/receipts/{receipt}/cancel.json
        resp_body['receipt'] = 'not found'
        resp_body['status'] = 0
        resp_body['errors'] = ['receipt not found; may be invalid or expired']
    else:
        resp_body['status'] = 1

    return 200 if resp_body['status'] == 1 else 400, headers, json.dumps(resp_body)


def subscription_migrate_callback(request):
    """A callback to mock the `/subscriptions/migrate.json` endpoint."""
    resp_body = {
        'request': TEST_REQUEST_ID
    }
    headers = {'X-Request-Id': TEST_REQUEST_ID}

    req_body = getattr(request, 'body', None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get('token', None) != TEST_TOKEN:
        resp_body['token'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['application token is invalid']
    elif qs.get('subscription', None) != TEST_SUBSCRIPTION_CODE:
        resp_body['subscription'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['subscription token is invalid']
    elif qs.get('user', None) != TEST_USER:
        resp_body['user'] = 'is not a valid user'
        resp_body['status'] = 0
        resp_body['errors'] = ['user key is not valid for any active user']
    else:
        resp_body['status'] = 1
        resp_body['subscribed_user_key'] = TEST_SUBSCRIBED_USER_KEY

    return 200 if resp_body['status'] == 1 else 400, headers, json.dumps(resp_body)


def groups_callback(request):
    """A callback to mock the `/groups/{group_key}.json` endpoint."""
    resp_body = {
        'request': TEST_REQUEST_ID
    }
    headers = {'X-Request-Id': TEST_REQUEST_ID}

    req_body = getattr(request, 'body', None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get('token', None) != TEST_TOKEN:
        resp_body['token'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['application token is invalid']
    elif request.path_url.split('/')[-1].split('.')[0] != TEST_GROUP:
        resp_body['group'] = 'not found'
        resp_body['status'] = 0
        resp_body['errors'] = ['group not found or you are not authorized to edit it']
    else:
        resp_body['status'] = 1
        resp_body['name'] = TEST_GROUP_NAME
        resp_body['users'] = [
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

    return 200 if resp_body['status'] == 1 else 400, headers, json.dumps(resp_body)


def groups_add_user_callback(request):
    """A callback to mock the `/groups/{group_id}/add_user.json` endpoint."""
    resp_body = {
        'request': TEST_REQUEST_ID
    }
    headers = {'X-Request-Id': TEST_REQUEST_ID}

    req_body = getattr(request, 'body', None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get('token', None) != TEST_TOKEN:
        resp_body['token'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['application token is invalid']
    elif request.path_url.split('/')[-2] != TEST_GROUP:
        resp_body['group'] = 'not found'
        resp_body['status'] = 0
        resp_body['errors'] = ['group not found or you are not authorized to edit it']
    elif qs.get('user', None) != TEST_USER:
        resp_body['user'] = 'invalid'
        resp_body['status'] = 0
        resp_body['errors'] = ['user key is invalid']
    else:
        resp_body['status'] = 1

    return 200 if resp_body['status'] == 1 else 400, headers, json.dumps(resp_body)
