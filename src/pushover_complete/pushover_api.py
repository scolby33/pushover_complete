"""The PushoverAPI class, containing the main functionality of the pushover_complete package."""

from .groups_api import _GroupsAPI
from .licensing_api import _LicensingAPI
from .message_api import _MessageAPI
from .receipt_and_callback_api import _ReceiptAndCallbackAPI
from .subscription_api import _SubscriptionAPI
from .user_group_validation_api import _UserGroupValidationAPI


class PushoverAPI(
    _MessageAPI,
    _UserGroupValidationAPI,
    _ReceiptAndCallbackAPI,
    _SubscriptionAPI,
    _GroupsAPI,
    _LicensingAPI,
):
    """
    The object representing an application interacting with the Pushover API.

    Instantiated with a Pushover application token.
    All API calls made via that instance will use the provided application token.

    :param token: A Pushover application token
    """
