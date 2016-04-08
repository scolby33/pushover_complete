import json
from urllib.parse import parse_qs

from tests.constants import *

def messages_callback(request):
    resp_body = {
        'status': 1,
        'request': TEST_REQUEST_ID
    }

    body = getattr(request, 'body', None)
    headers = {'X-Request-Id': TEST_REQUEST_ID}
    qs = parse_qs(body)

    if getattr(qs, 'priority', None) != 2:
        return 200, headers, json.dumps(resp_body)
    else:
        resp_body['receipt'] = 'rLqVuqTRh62UzxtmqiaLzQmVcPgiCy'
        return 200, headers, json.dumps(resp_body)

