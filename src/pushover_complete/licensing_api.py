from __future__ import annotations

from typing import Literal, Union, cast

from .apibase import ErrorResponse, SuccessResponse, _APIBase


class LicenseResponse(SuccessResponse):
    """A successful response from the Pushover API containing information about a license."""

    #: The number of credits available on the application
    credits: int


class _LicensingAPI(_APIBase):
    def assign_license(
        self, user_identifier: str, os: Literal["Android", "iOS", "Desktop"] | None = None
    ) -> LicenseResponse | ErrorResponse:
        """
        Assign a Pushover license to a user.

        :param user_identifier: A Pushover user key or email identifying the user to assign the license to
        :param os: An OS to limit the license

        :returns: Response body interpreted as JSON
        """
        payload = {}
        if "@" in user_identifier:
            payload["email"] = user_identifier
        else:
            payload["user"] = user_identifier
        if os:
            payload["os"] = os
        return cast(
            "Union[LicenseResponse, ErrorResponse]", self._generic_post("licenses/assign.json", payload=payload)
        )

    def check_license(self) -> LicenseResponse | ErrorResponse:
        return cast("Union[LicenseResponse, ErrorResponse]", self._generic_get("licenses.json"))
