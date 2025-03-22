"""Callbacks used by the :mod:`responses` module for mocking out API requests."""

import json

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs

from requests_toolbelt.multipart import decoder

from tests.constants import (
    SOUNDS,
    TEST_DEVICES,
    TEST_GROUP,
    TEST_GROUP_NAME,
    TEST_RECEIPT_ID,
    TEST_REQUEST_ID,
    TEST_SUBSCRIBED_USER_KEY,
    TEST_SUBSCRIPTION_CODE,
    TEST_TOKEN,
    TEST_USER,
    TEST_USER_EMAIL,
)


def get_content_disposition_name(headers):
    """Get the name from the Content-Disposition header (like `Content-Disposition: form-data; name="gotten name"`)."""
    content_disposition = headers[b"Content-Disposition"].decode("utf-8")
    name_and_label = content_disposition.split(";")[1]
    name = name_and_label.split("=")[1]
    return name.strip('"')


def generic_callback(request):
    """Mock callback for the _generic_get and _generic_post methods."""
    resp_body = {"status": 1}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("payload-test") is not None:
        resp_body["payload-test"] = qs.get("payload-test")
    else:
        resp_body["payload-test"] = False

    return 200, [], json.dumps(resp_body)


def messages_callback(request):  # noqa: PLR0912 -- it's hard to reduce the number of branches in this mock
    """Mock the `/messages.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    if getattr(request, "headers", {}).get("content-type") == "application/x-www-form-urlencoded":
        req_body = getattr(request, "body", None)
        qs = parse_qs(req_body)
        qs = {k: v[0] for k, v in qs.items()}
    else:
        request.content = getattr(request, "body", None)  # make this like MultipartDecoder.from_response expects
        multipart_data = decoder.MultipartDecoder.from_response(request)
        qs = {}
        for part in multipart_data.parts:
            header_name = get_content_disposition_name(part.headers)
            if header_name != "attachment":
                qs[header_name] = part.text
            else:
                qs[header_name] = part.content

    if qs.get("message") is None:
        resp_body["message"] = "cannot be blank"
        resp_body["status"] = 0
        resp_body["errors"] = ["message cannot be blank"]
    elif qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif qs.get("user") != TEST_USER and qs.get("user") != TEST_GROUP:  # allow TEST_USER or TEST_GROUP
        resp_body["user"] = "invalid"
        resp_body["status"] = 0
        resp_body["errors"] = ["user identifier is not a valid user, group, or subscribed user key"]
    elif qs.get("priority") == 2:  # noqa: PLR2004 -- TODO: this should probably be an enum
        if qs.get("expire") is None:
            resp_body["expire"] = "must be supplied with priority=2"
            resp_body["status"] = 0
            resp_body["errors"] = ["expire must be supplied with priority=2"]
        elif qs.get("retry") is None:
            resp_body["retry"] = "must be supplied with priority=2"
            resp_body["status"] = 0
            resp_body["errors"] = ["retry must be supplied with priority=2"]
        else:
            resp_body["receipt"] = TEST_RECEIPT_ID
    else:
        resp_body["status"] = 1

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def sounds_callback(request):
    """Mock the `/sounds.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    else:
        resp_body["status"] = 1
        resp_body["sounds"] = SOUNDS

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def validate_callback(request):
    """Mock the `/users/validate.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]

    user = qs.get("user")
    if user == TEST_USER:
        device = qs.get("device")
        if device and device.lower() not in TEST_DEVICES:
            resp_body["device"] = "invalid for this user"
            resp_body["status"] = 0
            resp_body["errors"] = ["device name is not valid for this user"]
        else:
            resp_body["status"] = 1
            resp_body["group"] = 0
            resp_body["devices"] = TEST_DEVICES
    elif user == TEST_GROUP:
        resp_body["status"] = 1
        resp_body["group"] = 1
        resp_body["devices"] = []
    else:
        resp_body["user"] = "invalid"
        resp_body["status"] = 0
        resp_body["errors"] = ["user identifier is not a valid user, group, or subscribed user key"]

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def receipt_callback(request):
    r"""
    Mock the /receipts/{receipt}.json endpoint.

    Best used like so::

        url_re = re.compile(r'https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*\.json')
        responses.add_callback(
            responses.GET,
            url_re,
            callback=receipt_callback,
            content_type='application/json'
        )

    in order to capture all calls to the endpoint.
    """
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif (
        request.path_url.split("/")[-1].split(".")[0] != TEST_RECEIPT_ID
    ):  # get the receipt from a url of the form /1/receipts/{receipt}.json
        resp_body["receipt"] = "not found"
        resp_body["status"] = 0
        resp_body["errors"] = ["receipt not found; may be invalid or expired"]
    else:
        resp_body["status"] = 1
        resp_body["acknowledged"] = 1
        resp_body["acknowledged_at"] = 100
        resp_body["acknowledged_by"] = TEST_USER
        resp_body["acknowledged_by_device"] = TEST_DEVICES[0]
        resp_body["last_delivered_at"] = 100
        resp_body["expired"] = 1
        resp_body["expires_at"] = 100
        resp_body["called_back"] = 0
        resp_body["called_back_at"] = 100

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def receipt_cancel_callback(request):
    r"""
    Mock the /receipts/{receipt}/cancel.json endpoint.

    Best used like so::

            url_re = re.compile(r'https://api\.pushover\.net/1/receipts/r[a-zA-Z0-9]*/cancel\.json')
        responses.add_callback(
            responses.GET,
            url_re,
            callback=receipt_cancel_callback,
            content_type='application/json'
        )

    in order to capture all calls to the endpoint.
    """
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif (
        request.path_url.split("/")[-2] != TEST_RECEIPT_ID
    ):  # get the receipt from a url of the form /1/receipts/{receipt}/cancel.json
        resp_body["receipt"] = "not found"
        resp_body["status"] = 0
        resp_body["errors"] = ["receipt not found; may be invalid or expired"]
    else:
        resp_body["status"] = 1

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def subscription_migrate_callback(request):
    """Mock the `/subscriptions/migrate.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif qs.get("subscription") != TEST_SUBSCRIPTION_CODE:
        resp_body["subscription"] = "invalid"
        resp_body["status"] = 0
        resp_body["errors"] = ["subscription token is invalid"]
    elif qs.get("user") != TEST_USER:
        resp_body["user"] = "is not a valid user"
        resp_body["status"] = 0
        resp_body["errors"] = ["user key is not valid for any active user"]
    else:
        resp_body["status"] = 1
        resp_body["subscribed_user_key"] = TEST_SUBSCRIBED_USER_KEY

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def groups_callback(request):
    """Mock the `/groups/{group_key}.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif request.path_url.split("/")[-1].split(".")[0] != TEST_GROUP:
        resp_body["group"] = "not found"
        resp_body["status"] = 0
        resp_body["errors"] = ["group not found or you are not authorized to edit it"]
    else:
        resp_body["status"] = 1
        resp_body["name"] = TEST_GROUP_NAME
        resp_body["users"] = [
            {
                "user": TEST_USER,
                "device": TEST_DEVICES[0],
                "memo": "",
                "disabled": False,
            },
            {
                "user": TEST_USER,
                "device": TEST_DEVICES[1],
                "memo": "",
                "disabled": False,
            },
        ]

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def groups_add_user_callback(request):
    """Mock the `/groups/{group_id}/add_user.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif request.path_url.split("/")[-2] != TEST_GROUP:
        resp_body["group"] = "not found"
        resp_body["status"] = 0
        resp_body["errors"] = ["group not found or you are not authorized to edit it"]
    elif qs.get("user") != TEST_USER:
        resp_body["user"] = "invalid"
        resp_body["status"] = 0
        resp_body["errors"] = ["user key is invalid"]
    else:
        resp_body["status"] = 1

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def groups_delete_user_callback(request):
    """Mock the `/groups/{group_id}/delete_user.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif request.path_url.split("/")[-2] != TEST_GROUP:
        resp_body["group"] = "not found"
        resp_body["status"] = 0
        resp_body["errors"] = ["group not found or you are not authorized to edit it"]
    elif qs.get("user") != TEST_USER:
        resp_body["user"] = "invalid"
        resp_body["status"] = 0
        resp_body["errors"] = ["user is not a member of this group"]
    else:
        resp_body["status"] = 1

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def groups_disable_user_callback(request):
    """Mock the `/groups/{group_id}/disable_user.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif request.path_url.split("/")[-2] != TEST_GROUP:
        resp_body["group"] = "not found"
        resp_body["status"] = 0
        resp_body["errors"] = ["group not found or you are not authorized to edit it"]
    elif qs.get("user") != TEST_USER:
        resp_body["user"] = "invalid"
        resp_body["status"] = 0
        resp_body["errors"] = ["user is not a member of this group"]
    else:
        resp_body["status"] = 1

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def groups_enable_user_callback(request):
    """Mock the `/groups/{group_id}/enable_user.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif request.path_url.split("/")[-2] != TEST_GROUP:
        resp_body["group"] = "not found"
        resp_body["status"] = 0
        resp_body["errors"] = ["group not found or you are not authorized to edit it"]
    elif qs.get("user") != TEST_USER:
        resp_body["user"] = "invalid"
        resp_body["status"] = 0
        resp_body["errors"] = ["user is not a member of this group"]
    else:
        resp_body["status"] = 1

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def groups_rename_callback(request):
    """Mock the `/groups/{group_id}/rename.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif request.path_url.split("/")[-2] != TEST_GROUP:
        resp_body["group"] = "not found"
        resp_body["status"] = 0
        resp_body["errors"] = ["group not found or you are not authorized to edit it"]
    else:
        resp_body["status"] = 1

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)


def licenses_assign_callback(request):
    """Mock the `/licenses/assign.json` endpoint."""
    resp_body = {"request": TEST_REQUEST_ID}
    headers = {"X-Request-Id": TEST_REQUEST_ID}

    req_body = getattr(request, "body", None)
    qs = parse_qs(req_body)
    qs = {k: v[0] for k, v in qs.items()}

    if qs.get("token") != TEST_TOKEN:
        resp_body["token"] = "invalid"  # noqa: S105 -- not a real secret
        resp_body["status"] = 0
        resp_body["errors"] = ["application token is invalid"]
    elif qs.get("email") is not None and qs.get("email") != TEST_USER_EMAIL:
        resp_body["email"] = "is not a valid e-mail address"
        resp_body["status"] = 0
        resp_body["errors"] = ["e-mail address is not a valid address"]
    elif qs.get("user") is not None and qs.get("user") != TEST_USER:
        resp_body["user"] = "is not a valid user"
        resp_body["status"] = 0
        resp_body["errors"] = ["user key is not valid for any active user"]
    elif qs.get("user") is None and qs.get("email") is None:
        resp_body["user"] = "must be supplied"
        resp_body["email"] = "must be supplied"
        resp_body["status"] = 0
        resp_body["errors"] = ["user or email must be supplied"]
    else:
        resp_body["status"] = 1
        resp_body["credits"] = 0

    return 200 if resp_body["status"] == 1 else 400, headers, json.dumps(resp_body)
