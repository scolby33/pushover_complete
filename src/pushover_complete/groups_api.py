from __future__ import annotations

from typing import TypedDict, Union, cast

from .apibase import ErrorResponse, SuccessResponse, _APIBase


class GroupCreateResponse(SuccessResponse):
    #: The key for the created group
    group: str


class GroupUser(TypedDict):
    """Information about a user who is a member of a group."""

    #: The user's token
    user: str
    device: str | None
    memo: str | None
    disabled: bool


class GroupInfoResponse(SuccessResponse):
    """A successful response from the Pushover API containing information about a group."""

    name: str
    users: list[GroupUser]


class GroupListInfo(TypedDict):
    name: str
    group: str


class GroupsListResponse(SuccessResponse):
    groups: list[GroupListInfo]


class _GroupsAPI(_APIBase):
    def group_create(self, name: str) -> GroupCreateResponse | ErrorResponse:
        return cast(
            "Union[GroupCreateResponse, ErrorResponse]",
            self._generic_post("groups.json", payload={"name": name}),
        )

    def groups_list(self) -> GroupsListResponse | ErrorResponse:
        return cast(
            "Union[GroupsListResponse, ErrorResponse]",
            self._generic_get("groups.json"),
        )

    def group_info(self, group_key: str) -> SuccessResponse | ErrorResponse:
        """
        Retrieve information about a delivery group.

        :param group_key: A Pushover group key

        :returns: Response body interpreted as JSON
        """
        return cast("Union[SuccessResponse, ErrorResponse]", self._generic_get("groups/{}.json", group_key))

    def group_add_user(
        self, group_key: str, user: str, device: str | None = None, memo: str | None = None
    ) -> SuccessResponse | ErrorResponse:
        """
        Add a user to a group.

        :param group_key: A Pushover group key
        :param user: The user key to be added to the group
        :param device: A string representing the device name to add to the group
        :param memo: A memo to store with the user's group membership (max 200 characters)

        :returns: Response body interpreted as JSON
        """
        payload = {"user": user, "device": device, "memo": memo}
        return cast(
            "Union[GroupInfoResponse, ErrorResponse]", self._generic_post("groups/{}/add_user.json", group_key, payload)
        )

    def group_delete_user(self, group_key: str, user: str) -> SuccessResponse | ErrorResponse:
        """
        Remove user from a group.

        :param group_key: A Pushover group key
        :param user: The user key to remove from the group

        :returns: Response body interpreted as JSON
        """
        payload = {"user": user}
        return cast(
            "Union[SuccessResponse, ErrorResponse]",
            self._generic_post("groups/{}/delete_user.json", group_key, payload),
        )

    def group_disable_user(self, group_key: str, user: str) -> SuccessResponse | ErrorResponse:
        """
        Temporarily disable a user in a group.

        :param group_key: A Pushover group key
        :param user: The user key to disable

        :returns: Response body interpreted as JSON
        """
        payload = {"user": user}
        return cast(
            "Union[SuccessResponse, ErrorResponse]",
            self._generic_post("groups/{}/disable_user.json", group_key, payload),
        )

    def group_enable_user(self, group_key: str, user: str) -> SuccessResponse | ErrorResponse:
        """
        Re-enable a user in a group.

        :param group_key: A Pushover group key
        :param user: The user key to enable

        :returns: Response body interpreted as JSON
        """
        payload = {"user": user}
        return cast(
            "Union[SuccessResponse, ErrorResponse]",
            self._generic_post("groups/{}/enable_user.json", group_key, payload),
        )

    def group_rename(self, group_key: str, new_name: str) -> SuccessResponse | ErrorResponse:
        """
        Change the name of a group.

        :param group_key: A Pushover group key
        :param new_name: The new name for the group

        :returns: Response body interpreted as JSON
        """
        payload = {"name": new_name}
        return cast(
            "Union[SuccessResponse, ErrorResponse]", self._generic_post("groups/{}/rename.json", group_key, payload)
        )
