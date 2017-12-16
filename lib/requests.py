import json
from functools import wraps
from urllib.request import Request, urlopen

from lib import const


def response_to_python(func):
    """
    Decorator converts json data to python data.
    """
    @wraps(func)
    def json_to_python():
        return json.loads(func())

    return json_to_python


class LinkedinRequest(object):
    def __init__(self, token, url, method=const.GET):
        self.token = token
        self.url = url
        self.method = method

    @property
    def headers(self):
        """
        Set here all headers what you need to send to Linkedin endpoints.
        """
        return {
            "Authorization": "Bearer {token}".format(token=self.token),
            "Accept-Language": "es-ES, en-US, it-IT",
        }

    @response_to_python
    def retrieve(self):
        """
        Returns response content.
        """
        request = Request(url=self.url, method=self.method, headers=self.headers)

        return urlopen(request).read().decode()


def retrieve_basic_profile_data(token):
    url = "https://api.linkedin.com/v1/people/~?format=json"
    request = LinkedinRequest(token, url)

    return request.retrieve()
