import requests

from linkedin_py import const
from linkedin_py.authentication.main import Authentication
from linkedin_py.utils import validate_response


class LinkedinClient(object):
    def __init__(self, token, url, method=const.GET):
        self.token = token
        self.url = url
        self.method = method

    @validate_response
    def retrieve(self):
        """
        Returns response content.
        """
        authentication = Authentication(self.token)
        return requests.get(url=self.url, headers=authentication.get_headers())
