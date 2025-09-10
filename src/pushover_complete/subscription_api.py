from __future__ import annotations

import sys
from typing import TYPE_CHECKING, TypedDict, Union, cast

import requests

from .apibase import ErrorResponse, SuccessResponse, _APIBase

if sys.version_info >= (3, 11):
    from typing import Unpack
else:
    from typing_extensions import Unpack

if TYPE_CHECKING:
    from collections.abc import Iterable


class UserSubscriptionRequest(TypedDict, total=False):
    """A representation of the data that can be submitted to migrate a user to a subscription."""

    #: The name of the user's device that the subscription should be limited to
    device: str
    #: The user's preferred default sound
    sound: str


class MultiUserSubscriptionRequest(UserSubscriptionRequest):
    """
    Like a :class:`UserSubscriptionRequest`, but also containing the user token.

    Used for submitting a group of users to subscribe to at once.
    """

    user: str


class SubscriptionResponse(SuccessResponse):
    """
    A response from the Pushover API for a successful subscription migration request.

    You should definitely save the :attr:`SubscriptionResponse.subscribed_user_key` in place of the user's
    original key.
    """

    subscribed_user_key: str


class _SubscriptionAPI(_APIBase):
    def _migrate_to_subscription(
        self,
        user: str,
        subscription_code: str,
        *,
        session: requests.Session | None = None,
        **subscription_request: Unpack[UserSubscriptionRequest],
    ) -> SubscriptionResponse | ErrorResponse:
        """
        Migrates a user key to a subscription key.

        Takes a ``session`` parameter to use for sending HTTP requests, allowing the re-use of sessions to decrease
        overhead.
        Used to abstract the differences between :meth:`PushoverAPI.migrate_to_subscription` and
        :meth:`PushoverAPI.migrate_multiple_to_subscription`.
        Feel free to call directly if your use case isn't fulfilled by the more public methods.

        :param user: The Pushover user token to be migrated
        :param subscription_code: The subscription code to migrate the user to
        :param session: A :class:`requests.Session` object to be used to send HTTP requests. Useful to send multiple
            messages without opening multiple HTTP sessions.
        :param subscription_request: The subscription request to be sent

        :returns: Response body interpreted as JSON
        """
        payload = {
            "user": user,
            "subscription": subscription_code,
            **subscription_request,
        }
        if "device" in payload:
            payload["device_name"] = payload.pop("device")

        return cast(
            "Union[SubscriptionResponse, ErrorResponse]",
            self._generic_post("subscriptions/migrate.json", payload=payload, session=session),
        )

    def migrate_to_subscription(
        self, user: str, subscription_code: str, **subscription_request: Unpack[UserSubscriptionRequest]
    ) -> SubscriptionResponse | ErrorResponse:
        """
        Migrate a user key to a subscription key.

        :param user: The Pushover user token to be migrated
        :param subscription_code: The subscription code to migrate the user to
        :param subscription_request: The subscription request to be sent

        :returns: Response body interpreted as JSON
        """
        return self._migrate_to_subscription(user, subscription_code, **subscription_request)

    def migrate_multiple_to_subscription(
        self, subscription_requests: Iterable[MultiUserSubscriptionRequest], subscription_code: str
    ) -> list[SubscriptionResponse | ErrorResponse]:
        """
        Migrate multiple users to subscriptions with one call. Utilizes a single HTTP session to decrease overhead.

        :param subscription_requests: An iterable of subscription requests to be sent
        :param subscription_code: The subscription code to migrate the users to

        :returns: Response body interpreted as JSON
        """
        sess = requests.Session()
        return [
            self._migrate_to_subscription(session=sess, subscription_code=subscription_code, **subscription_request)
            for subscription_request in subscription_requests
        ]
