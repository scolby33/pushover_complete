# ruff: noqa: FA100
# Can't use from __future__ import annotations
# because this breaks the introspection of the NotRequired[]
# field(s) in the TypedDicts.

import sys
from typing import Any, Literal, Optional, TypedDict, Union
from urllib.parse import urljoin
from uuid import UUID

import requests

from .error import BadAPIRequestError

if sys.version_info >= (3, 11):
    from typing import NotRequired, TypeAlias
else:
    from typing_extensions import NotRequired, TypeAlias

PUSHOVER_API_URL = "https://api.pushover.net/1/"

#: Value returned by the Pushover API to indicate success
ResponseStatusSuccess: TypeAlias = Literal[1]
#: Value returned by the Pushover API to indicate failure
ResponseStatusError: TypeAlias = Literal[0]


class SuccessResponse(TypedDict):
    """A response from the Pushover API for a successful request."""

    #: The status of the request; always ``1``
    status: ResponseStatusSuccess
    #: The request identifier
    request: UUID  # TODO: convert to actual UUID type in return values


class ErrorResponse(TypedDict):
    """
    A response from the Pushover API for a failed request.

    Additional fields may be present describing problems with specific fields of the request.
    """

    #: The status of the request; always ``0``
    status: ResponseStatusError
    #: The request identifier
    request: UUID
    #: A list of error messages
    errors: NotRequired[list[str]]


class _APIBase:
    def __init__(self, token: str):
        self.token = token

    def _generic_get(
        self,
        endpoint: str,
        url_parameter: Optional[str] = None,
        payload: Optional[dict[str, Any]] = None,
        session: Optional[requests.Session] = None,
    ) -> Union[SuccessResponse, ErrorResponse]:
        """
        Make a GET request to the Pushover API.

        :param endpoint: The endpoint of the API to hit. Will be joined with "https://api.pushover.net/1/". Example
            value: "groups/{}.json"
        :param url_parameter: A parameter to replace in the endpoint string provided. Example value: "g123456". Combined
            with the above example value, would result in a final URL of
            "https://api.pushover.net/1/groups/g123456.json"
        :param payload: A dict of parameters to be appended to the URL, e.g. :code:`{'test-param': False}` would result
            in the URL having :code:`?test-param=false` appended. Do not include the application token in this dict, as
            it is added by the function.
        :param session: A :class:`requests.Session` object to be used to send HTTP requests.

        :returns: Response body interpreted as JSON
        :raises BadAPIRequestError: Raised when the Pushover response body contains a status code other than 1.
        """
        if payload is None:
            payload = {}
        payload["token"] = self.token

        get = session.get if session else requests.get
        resp = get(urljoin(PUSHOVER_API_URL, endpoint.format(url_parameter)), data=payload)
        resp_body = resp.json()
        if resp_body.get("status", None) != 1:
            msg = "{}: {}".format(resp.status_code, ": ".join(resp_body.get("errors")))
            raise BadAPIRequestError(msg)
        return resp_body

    def _generic_post(
        self,
        endpoint: str,
        url_parameter: Optional[str] = None,
        payload: Optional[dict[str, Any]] = None,
        session: Optional[requests.Session] = None,
        files: Optional[dict[str, Any]] = None,
    ) -> Union[SuccessResponse, ErrorResponse]:
        """
        Make a POST request to the Pushover API.

        :param endpoint: The endpoint of the API to hit. Will be joined with "https://api.pushover.net/1/".
            Example value: "groups/{}.json".
        :param url_parameter: A parameter to replace in the endpoint string provided. Example value: "g123456". Combined
            with the above example value, would result in a final URL of
            "https://api.pushover.net/1/groups/g123456.json".
        :param payload: A dict of parameters to be appended to the URL, e.g. :code:`{'test-param': False}` would result
            in the URL having :code:`?test-param=false` appended. Do not include the application token in this dict, as
            it is added by the function.
        :param files: (optional) A dict of ``'attachment': value`` for attachment to the message. ``value`` may be a
            file-like object, or a tuple of at least
            ``('filename', file-like[, 'content_type'[, custom_headers_dict]])``. The optional 'content_type' string
            describes the file type and custom_headers_dict is a dict-like-object with additional headers describing
            the file.
        :param session: A :class:`requests.Session` object to be used to send HTTP requests.
        :type files: dict{str, file-like} or dict{str, tuple(str, file-like[, str[, dict]])}

        :returns: Response body interpreted as JSON
        :raises BadAPIRequestError: Raised when the Pushover response body contains a status code other than 1.
        """
        if payload is None:
            payload = {}
        payload["token"] = self.token

        post = session.post if session else requests.post
        resp = post(
            urljoin(PUSHOVER_API_URL, endpoint.format(url_parameter)),
            data=payload,
            files=files,
        )
        resp_body = resp.json()
        if resp_body.get("status", None) != 1:
            msg = "{}: {}".format(resp.status_code, ": ".join(resp_body.get("errors")))
            raise BadAPIRequestError(msg)
        return resp_body
