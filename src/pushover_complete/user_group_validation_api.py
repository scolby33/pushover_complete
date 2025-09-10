"""Implementation of Pushover's User/Group Validation API."""

from __future__ import annotations

from typing import Union, cast

from .apibase import ErrorResponse, SuccessResponse, _APIBase


class UserValidationResponse(SuccessResponse):
    """A response from the Pushover API for a successful user validation request."""

    devices: list[str]
    licenses: list[str]


class _UserGroupValidationAPI(_APIBase):
    def validate(self, user: str, device: str | None = None) -> UserValidationResponse | ErrorResponse:
        """
        Validate a user or group token or a user device.

        :param user: A Pushover user or group token to validate
        :param device: A string representing a device name to validate

        :returns: Response body interpreted as JSON
        """
        payload = {"user": user, "device": device}
        return cast(
            "Union[UserValidationResponse, ErrorResponse]", self._generic_post("users/validate.json", payload=payload)
        )
