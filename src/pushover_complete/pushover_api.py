try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests

from .error import BadAPIRequestError

PUSHOVER_API_URL = 'https://api.pushover.net/1/'


class PushoverAPI(object):
    """The object representing an application interacting with the Pushover API.
    Instantiated with a Pushover application token.
    All API calls made via that instance will use the provided application token.

    :param token: A Pushover application token
    :type token: str
    """
    def __init__(self, token):
        self.token = token

    def _generic_get(self, endpoint, url_parameter=None, payload=None, session=None):
        """A method for abstracting GET requests to the Pushover API.

        :param endpoint: The endpoint of the API to hit. Will be joined with "https://api.pushover.net/1/". Example value: "groups/{}.json"
        :param url_parameter: A parameter to replace in the endpoint string provided. Example value: "g123456". Combined with the above example value, would result in a final URL of "https://api.pushover.net/1/groups/g123456.json"
        :param payload: A dict of parameters to be appended to the URL, e.g. :code:`{'test-param': False}` would result in the URL having :code:`?test-param=false` appended. Do not include the application token in this dict, as it is added by the function.
        :param session: A :class:`requests.Session` object to be used to send HTTP requests.
        :type endpoint: str
        :type url_parameter: str
        :type payload: dict
        :type session: requests.Session

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        if payload is None:
            payload = {}
        payload['token'] = self.token

        get = session.get if session else requests.get
        resp = get(
            urljoin(PUSHOVER_API_URL, endpoint.format(url_parameter)),
            data=payload
        )
        resp_body = resp.json()
        if resp_body.get('status', None) != 1:
            raise BadAPIRequestError('{}: {}'.format(resp.status_code, ': '.join(resp_body.get('errors'))))
        return resp_body

    def _generic_post(self, endpoint, url_parameter=None, payload=None, session=None):
        """A method for abstracting POST requests to the Pushover API.

        :param endpoint: The endpoint of the API to hit. Will be joined with "https://api.pushover.net/1/". Example value: "groups/{}.json"
        :param url_parameter: A parameter to replace in the endpoint string provided. Example value: "g123456". Combined with the above example value, would result in a final URL of "https://api.pushover.net/1/groups/g123456.json"
        :param payload: A dict of parameters to be appended to the URL, e.g. :code:`{'test-param': False}` would result in the URL having :code:`?test-param=false` appended. Do not include the application token in this dict, as it is added by the function.
        :param session: A :class:`requests.Session` object to be used to send HTTP requests.
        :type endpoint: str
        :type url_parameter: str
        :type payload: dict
        :type session: requests.Session

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        if payload is None:
            payload = {}
        payload['token'] = self.token
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        post = session.post if session else requests.post
        resp = post(
            urljoin(PUSHOVER_API_URL, endpoint.format(url_parameter)),
            data=payload,
            headers=headers
        )
        resp_body = resp.json()
        if resp_body.get('status', None) != 1:
            raise BadAPIRequestError('{}: {}'.format(resp.status_code, ': '.join(resp_body.get('errors'))))
        return resp_body

    def _send_message(self, user, message, device=None, title=None, url=None, url_title=None,
                      priority=None, retry=None, expire=None, callback_url=None, timestamp=None, sound=None, html=False,
                      session=None):
        """The internal function used to send messages via the Pushover API.
        Takes a ``session`` parameter to use for sending HTTP requests, allowing the re-use of sessions to decrease overhead.
        Used to abstract the differences between :meth:`PushoverAPI.send_message` and :meth:`PushoverAPI.send_messages`.
        Feel free to call directly if your use case isn't fulfilled by the more public methods.

        :param user: A Pushover user token representing the user or group to whom the message will be sent
        :param message: The message to be sent
        :param device: A string or iterable representing the device(s) to which the message will be sent
        :param title: The title of the message
        :param url: A URL to be included with the message
        :param url_title: The link text to be displayed for the URL. If omitted, the URL itself is displayed.
        :param priority: An integer representing the priority of the message, from -2 (least important) to 2 (emergency). Default is 0.
        :param retry: How often the Pushover server will re-send an emergency-priority message in seconds. Required with priority 2 messages.
        :param expire: How long an emergency-priority message will be re-sent for in seconds
        :param callback_url: A url to be visited by the Pushover servers upon acknowledgement of an emergency-priority message
        :param timestamp: A Unix timestamp of the message's date and time to be displayed instead of the time the message is received by the Pushover servers
        :param sound: A string representing a sound to be played with the message instead of the user's default
        :param html: An integer representing if HTML formatting will be enabled for the message text. Set to 1 to enable.
        :param session: A :class:`requests.Session` object to be used to send HTTP requests. Useful to send multiple messages without opening multiple HTTP sessions.
        :type user: str
        :type message: str
        :type device: str or list
        :type title: str
        :type url: str
        :type url_title: str
        :type priority: int
        :type retry: int
        :type expire: int
        :type callback_url: str
        :type timestamp: int
        :type sound: str
        :type html: int
        :type session: requests.Session

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        payload = {
            'user': user,
            'message': message,
            'device': device,
            'title': title,
            'url': url,
            'url_title': url_title,
            'priority': priority,
            'retry': retry,
            'expire': expire,
            'callback': callback_url,
            'timestamp': timestamp,
            'sound': sound,
            'html': html
        }

        return self._generic_post('messages.json', payload=payload, session=session)

    def send_message(self, user, message, device=None, title=None, url=None, url_title=None,
                     priority=None, retry=None, expire=None, callback_url=None, timestamp=None, sound=None, html=False):
        """Send a message via the Pushover API.

        :param user: A Pushover user token representing the user or group to whom the message will be sent
        :param message: The message to be sent
        :param device: A string or iterable representing the device(s) to which the message will be sent
        :param title: The title of the message
        :param url: A URL to be included with the message
        :param url_title: The link text to be displayed for the URL. If omitted, the URL itself is displayed.
        :param priority: An integer representing the priority of the message, from -2 (least important) to 2 (emergency). Default is 0.
        :param retry: How often the Pushover server will re-send an emergency-priority message in seconds. Required with priority 2 messages.
        :param expire: How long an emergency-priority message will be re-sent for in seconds
        :param callback_url: A url to be visited by the Pushover servers upon acknowledgement of an emergency-priority message
        :param timestamp: A Unix timestamp of the message's date and time to be displayed instead of the time the message is received by the Pushover servers
        :param sound: A string representing the sound to be played with the message instead of the user's default. Available sounds can be retreived using :meth:`PushoverAPI.get_sounds`.
        :param html: An integer representing if HTML formatting will be enabled for the message text. Set to 1 to enable.
        :type user: str
        :type message: str
        :type device: str or list
        :type title: str
        :type url: str
        :type url_title: str
        :type priority: int
        :type retry: int
        :type expire: int
        :type callback_url: str
        :type timestamp: int
        :type sound: str
        :type html: int

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        return self._send_message(user, message, device, title, url, url_title, priority, retry, expire, callback_url,
                                  timestamp, sound, html)

    def send_messages(self, messages):
        """Send multiple messages with one call. Utilizes a single HTTP session to decrease overhead.

        :param messages: An iterable of messages to be sent. Each item in the iterable must be expandable using the ``**kwargs`` syntax with the keys matching the parameters of :meth:`PushoverAPI.send_message`.

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        sess = requests.Session()
        resp_bodies = []
        for message in messages:
            resp_bodies.append(self._send_message(session=sess, **message))
        return resp_bodies

    def get_sounds(self):
        """Get the current list of supported sounds from the Pushover servers.

        :return: A :class:`dict` of sounds, with keys representing the identifier and values a human-readable name.
        :rtype: dict
        """
        return self._generic_get('sounds.json').get('sounds')

    def validate(self, user, device=None):
        """Validate a user or group token or a user device.

        :param user: A Pushover user or group token to validate
        :param device: A string representing a device name to validate
        :type user: str
        :type device: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        payload = {
            'user': user,
            'device': device
        }
        return self._generic_post('users/validate.json', payload=payload)

    def check_receipt(self, receipt):
        """Check a receipt issued after sending an emergency-priority message.

        :param receipt: The receipt id
        :type receipt: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        return self._generic_get('receipts/{}.json', receipt)

    def cancel_receipt(self, receipt):
        """Cancel a receipt (and thus further re-sends of the message).

        :param receipt: The id of the receipt id to be cancelled
        :type receipt: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        return self._generic_post('receipts/{}/cancel.json', receipt)

    def _migrate_to_subscription(self, user, subscription_code, device=None, sound=None, session=None):
        """The internal function to migrate a user key to a subscription key.
        Takes a ``session`` parameter to use for sending HTTP requests, allowing the re-use of sessions to decrease overhead.
        Used to abstract the differences between :meth:`PushoverAPI.migrate_to_subscription` and :meth:`PushoverAPI.migrate_multiple_to_subscription`.
        Feel free to call directly if your use case isn't fulfilled by the more public methods.

        :param user: The user key to migrate
        :param subscription_code: The subscription code to migrate the user to
        :param device: The user's device that the subscription will be limited to
        :param sound: The user's preferred sound
        :param session: A :class:`requests.Session` object to be used to send HTTP requests. Useful to send multiple messages without opening multiple HTTP sessions.
        :type user: str
        :type subscription_code: str
        :type device: str
        :type sound: str
        :type session: requests.Session

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        payload = {
            'user': user,
            'subscription': subscription_code,
            'device_name': device,
            'sound': sound
        }

        return self._generic_post('subscriptions/migrate.json', payload=payload, session=session)

    def migrate_to_subscription(self, user, subscription_code, device=None, sound=None):
        """Migrate a user key to a subscription key.

        :param user: The user key to migrate
        :param subscription_code: The subscription code to migrate the user to
        :param device: The user's device that the subscription will be limited to
        :param sound: The user's preferred sound
        :type user: str
        :type subscription_code: str
        :type device: str
        :type sound: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        return self._migrate_to_subscription(user, subscription_code, device, sound)

    def migrate_multiple_to_subscription(self, users, subscription_code):
        """Migrate multiple users to subscriptions with one call. Utilizes a single HTTP session to decrease overhead.

        :param users: An iterable of messages to be sent. Each item in the iterable must be expandable using the ``**kwargs`` syntax with keys matching ``user`` and, optionally, ``device`` and ``sound``. Compare to :meth:`PushoverAPI.migrate_to_subscription`.
        :param subscription_code: The subscription code to migrate the user to
        :type subscription_code: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        sess = requests.Session()
        resps = []
        for user in users:
            resps.append(self._migrate_to_subscription(session=sess, subscription_code=subscription_code, **user))
        return resps

    def group_info(self, group_key):
        """Retrieve information about a delivery group.

        :param group_key: A Pushover group key
        :type group_key: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        return self._generic_get('groups/{}.json', group_key)

    def group_add_user(self, group_key, user, device=None, memo=None):
        """Add a user to a group.

        :param group_key: A Pushover group key
        :param user: The user key to be added to the group
        :param device: A string representing the device name to add to the group
        :param memo: A memo to store with the user's group membership (max 200 characters)
        :type group_key: str
        :type user: str
        :type device: str
        :type memo: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        payload = {
            'user': user,
            'device': device,
            'memo': memo
        }
        return self._generic_post('groups/{}/add_user.json', group_key, payload)

    def group_delete_user(self, group_key, user):
        """Remove user from a group.

        :param group_key: A Pushover group key
        :param user: The user key to remove from the group
        :type group_key: str
        :type user: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        payload = {
            'user': user
        }
        return self._generic_post('groups/{}/delete_user.json', group_key, payload)

    def group_disable_user(self, group_key, user):
        """Temporarily disable a user in a group.

        :param group_key: A Pushover group key
        :param user: The user key to disable
        :type group_key: str
        :type user: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        payload = {
            'user': user
        }
        return self._generic_post('groups/{}/disable_user.json', group_key, payload)

    def group_enable_user(self, group_key, user):
        """Re-enable a user in a group.

        :param group_key: A Pushover group key
        :param user: The user key to enable
        :type group_key: str
        :type user: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        payload = {
            'user': user
        }
        return self._generic_post('groups/{}/enable_user.json', group_key, payload)

    def group_rename(self, group_key, new_name):
        """Change the name of a group.

        :param group_key: A Pushover group key
        :param new_name: The new name for the group
        :type group_key: str
        :type new_name: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        payload = {
            'name': new_name
        }
        return self._generic_post('groups/{}/rename.json', group_key, payload)

    def assign_license(self, user_identifier, os=None):
        """Assign a Pushover license to a user.

        :param user_identifier: A Pushover user key or email identifying the user to assign the license to
        :param os: An OS to limit the license. Available options are :code:`Android`, :code:`iOS`, or :code:`Desktop`
        :type user_identifier: str
        :type os: str

        :returns: Response body interpreted as JSON
        :rtype: dict
        """
        payload = {
            'os': os
        }
        if '@' in user_identifier:
            payload['email'] = user_identifier
        else:
            payload['user'] = user_identifier
        return self._generic_post('licenses/assign.json', payload=payload)
