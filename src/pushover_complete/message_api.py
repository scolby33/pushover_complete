"""Implementation of Pushover's Messages API."""

# ruff: noqa: FA100
# Can't use from __future__ import annotations
# because this breaks the introspection of the NotRequired[]
# field(s) in the TypedDicts.

import sys
from collections.abc import Iterable
from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO, Literal, Optional, TypedDict, Union, cast

import requests

from .apibase import ErrorResponse, SuccessResponse, _APIBase

if sys.version_info >= (3, 11):
    from typing import NotRequired, TypeAlias, Unpack
else:
    from typing_extensions import NotRequired, TypeAlias, Unpack


class MessageRequest(TypedDict, total=False):
    """A representation of the data that can be submitted to send a Pushover message."""

    # TODO: check these parameters all exist, and that all existing params are here
    #: A string or iterable representing the device(s) to which the message will be sent
    device: Union[str, list[str], None]
    #: The title of the message
    title: Union[str, None]
    #: A URL to be included with the message
    url: Union[str, None]
    #: The link text to be displayed for the URL. If omitted, the URL itself is displayed.
    url_title: Union[str, None]
    #: The file path pointing to the image to be attached to the message or a file-like-object representing the image
    #: data.
    image: Union[str, Path, BinaryIO, None]
    #: An integer representing the priority of the message, from -2 (least important) to 2 (emergency). Default is 0.
    priority: Union[int, None]
    #: How often the Pushover service will re-send an emergency-priority message in seconds. Required with priority 2
    #: messages.
    retry: Union[int, None]
    #: How long an emergency-priority message will be re-sent for in seconds
    expire: Union[int, None]
    #: A url to be visited by the Pushover servers upon acknowledgement of an emergency-priority
    callback_url: Union[str, None]
    #: A Unix timestamp of the message's date and time to be displayed instead of the time the
    timestamp: Union[int, None]
    #: A string representing a sound to be played with the message instead of the user's default
    sound: Union[str, None]
    #: An integer representing if HTML formatting will be enabled for the message text. Set to 1 to enable, leave out
    #: to not enable.
    html: Union[Literal[1], None]
    #: An integer representing Time to Live in seconds, after which the message will be automatically deleted.
    ttl: Union[int, None]


def _to_payload(user: str, message: str, payload: MessageRequest) -> dict[str, Any]:
    """
    Create a dict appropriate for passing to the Message API.

    :param user: The user token
    :param message: The message
    :param payload: The rest of the message request

    :returns: The constructed payload
    """
    return {
        "user": user,
        "message": message,
        **payload,
    }


class MultiMessageRequest(MessageRequest):
    """
    Like a :class:`MessageRequest`, but also containing the user token.

    Used for submitting a group of messages to send at once.
    """

    #: The user token
    user: str
    #: The message to send
    message: str


class MessageResponse(SuccessResponse):
    """A response from the Pushover API for a successful message push request."""

    #: The receipt value if the message was sent at emergency priority
    receipt: NotRequired[str]


#: The name of a selectable sound
SoundName: TypeAlias = str
#: A description of the sound
SoundDescription: TypeAlias = str
#: A response from the Pushover API detailing the available sounds
SoundsResponse: TypeAlias = dict[SoundName, SoundDescription]


class LimitsResponse(SuccessResponse):
    """A response from the Pushover API for a successful limits query request."""

    #: Messages per month limit for the application
    limit: int
    #: The number of remaining messages for the month
    remaining: int
    #: Unix timestamp of when the count will reset
    reset: int


class _MessageAPI(_APIBase):
    def _send_message(
        self,
        user: str,
        message: str,
        *,
        session: Optional[requests.Session] = None,
        **payload: Unpack[MessageRequest],
    ) -> Union[MessageResponse, ErrorResponse]:
        """
        Send a message via the Pushover API with control over the HTTP session.

        Takes a ``session`` parameter to use for sending HTTP requests, allowing the re-use of sessions to decrease
        overhead.
        Used to abstract the differences between :meth:`PushoverAPI.send_message` and :meth:`PushoverAPI.send_messages`.
        Feel free to call directly if your use case isn't fulfilled by the more public methods.

        :param user: A Pushover user token representing the user or group to whom the message will be sent
        :param message: The message to be sent
        :param session: A :class:`requests.Session` object to be used to send HTTP requests. Useful to send multiple
            messages without opening multiple HTTP sessions.

        :returns: Response body interpreted as JSON
        """
        if image := payload.pop("image", None):
            # if it's a str or Path, open it
            if isinstance(image, (str, Path)):
                with Path(image).open("rb") as f:
                    return cast(
                        "Union[MessageResponse, ErrorResponse]",
                        self._generic_post(
                            "messages.json",
                            payload=_to_payload(user, message, payload),
                            session=session,
                            files={"attachment": f},
                        ),
                    )
            elif isinstance(image, BytesIO):
                return cast(
                    "Union[MessageResponse, ErrorResponse]",
                    self._generic_post(
                        "messages.json",
                        payload=_to_payload(user, message, payload),
                        session=session,
                        files={"attachment": image},
                    ),
                )
            else:
                msg = "image must be str, Path, or an open file-like"
                raise TypeError(msg)

        return cast(
            "Union[MessageResponse, ErrorResponse]",
            self._generic_post("messages.json", payload=_to_payload(user, message, payload), session=session),
        )

    def send_message(
        self,
        user: str,
        message: str,
        **payload: Unpack[MessageRequest],
    ) -> Union[MessageResponse, ErrorResponse]:
        """
        Send a message via the Pushover API.

        :param user: A Pushover user token representing the user or group to whom the message will be sent
        :param message: The message to be sent

        :returns: Response body interpreted as JSON
        """
        return self._send_message(user, message, **payload)

    def send_messages(self, messages: Iterable[MultiMessageRequest]) -> list[Union[MessageResponse, ErrorResponse]]:
        """
        Send multiple messages with one call. Utilizes a single HTTP session to decrease overhead.

        :param messages: An iterable of messages to be sent. Each item in the iterable must be expandable using the
            ``**kwargs`` syntax with the keys matching the parameters of :meth:`PushoverAPI.send_message`.

        :returns: Response body interpreted as JSON
        """
        with requests.Session() as sess:
            return [self._send_message(session=sess, **message) for message in messages]

    def get_sounds(self) -> SoundsResponse:
        """
        Get the current list of supported sounds from the Pushover servers.

        :return: A :class:`dict` of sounds, with keys representing the identifier and values a human-readable name.
        """
        # TODO: handle error case where no sounds were returned
        return cast("SoundsResponse", self._generic_get("sounds.json").get("sounds"))

    def get_limits(self) -> Union[LimitsResponse, ErrorResponse]:
        """
        Get the current message limit and remaining quota for the application.

        :returns: The limits
        """
        return cast("Union[LimitsResponse, ErrorResponse]", self._generic_get("limits.json"))
