"""Implementation of Pushover's Receipts and Callbacks API."""

from __future__ import annotations

import sys
from typing import Literal, Union, cast

from .apibase import ErrorResponse, SuccessResponse, _APIBase

if sys.version_info >= (3, 11):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

AcknowledgeStatusAcknowledged: TypeAlias = Literal[1]
AcknowledgeStatusUnacknowledged: TypeAlias = Literal[0]
AcknowledgeStatus = Union[AcknowledgeStatusAcknowledged, AcknowledgeStatusUnacknowledged]

ExpiredStatusExpired: TypeAlias = Literal[1]
ExpiredStatusUnexpired: TypeAlias = Literal[0]
ExpiredStatus = Union[ExpiredStatusExpired, ExpiredStatusUnexpired]

CallbackStatusCalledBack: TypeAlias = Literal[1]
CallbackStatusNotCalledBack: TypeAlias = Literal[0]
CallbackStatus = Union[CallbackStatusCalledBack, CallbackStatusNotCalledBack]


class ReceiptResponse(SuccessResponse):
    """A response from the Pushover API for a successful receipt check request."""

    acknowledged: AcknowledgeStatus
    acknowledged_at: int
    acknowledged_by: str
    acknowledged_by_device: str
    last_delivered_at: int
    expired: ExpiredStatus
    expires_at: int
    called_back: CallbackStatus
    called_back_at: int


class _ReceiptAndCallbackAPI(_APIBase):
    def check_receipt(self, receipt: str) -> ReceiptResponse | ErrorResponse:
        """
        Check a receipt issued after sending an emergency-priority message.

        :param receipt: The receipt id

        :returns: Response body interpreted as JSON
        """
        return cast("Union[ReceiptResponse, ErrorResponse]", self._generic_get("receipts/{}.json", receipt))

    def cancel_receipt(self, receipt: str) -> SuccessResponse | ErrorResponse:
        """
        Cancel a receipt (and thus further re-sends of the message).

        :param receipt: The id of the receipt id to be cancelled

        :returns: Response body interpreted as JSON
        """
        return self._generic_post("receipts/{}/cancel.json", receipt)

    def cancel_receipt_by_tags(self, tag: str) -> SuccessResponse | ErrorResponse:
        return cast(
            "Union[SuccessResponse, ErrorResponse]",
            self._generic_post("receipts/cancel_by_tag/{}.json", tag, None),
        )
