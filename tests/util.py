import json
from urllib.parse import parse_qs

from tests.constants import *


def messages_callback(request):
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
    elif qs.get('user', None) != TEST_USER:
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


def validate_callback(request):
    resp_body = {
        'status': 1,
        'request': TEST_REQUEST_ID,
        'devices': []
    }

    body = getattr(request, 'body', None)
    headers = {'X-Request-Id': TEST_REQUEST_ID}
    qs = parse_qs(body)

    if getattr(qs, 'user', str()).startswith('u'):
        resp_body['group'] = 0
    elif getattr(qs, 'user', str()).startswith('g'):
        resp_body['group'] = 1

    return 200, headers, json.dumps(resp_body)

