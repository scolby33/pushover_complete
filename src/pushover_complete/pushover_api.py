import requests

from .error import PushoverCompleteError

class PushoverAPI(object):
    def __init__(self, token):
        self.token = token

    def send_message(self, user, message, device=None, title=None, url=None, url_title=None,
                     priority=None, retry=None, expire=None, timestamp=None, sound=None, html=False):
        if priority == 2:
            if retry is None or expire is None:
                raise PushoverCompleteError('Must specify `retry` and `expire` with priority 2.')
        payload = {
            'token': self.token,
            'user': user,
            'message': message,
            'device': device,
            'title': title,
            'url': url,
            'url_title': url_title,
            'priority': priority,
            'retry': retry,
            'expire': expire,
            'timestamp': timestamp,
            'sound': sound,
            'html': html
        }
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        r = requests.post(
            'https://api.pushover.net/1/messages.json',
            data=payload,
            headers=headers
        )
        return r
