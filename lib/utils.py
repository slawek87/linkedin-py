from functools import wraps

import re
import requests

from lib.authorization.exceptions import AuthorizationRejected

JSON = 'json'


def prepare_url(url, params, response_format=JSON):
    """
    Function prepares url with Linkedin's standards.
    """
    r_unwanted = re.compile("[\s\n\t\r]")
    params = r_unwanted.sub("", params)

    url = "{url}{params}".format(url=url, params=params)

    if response_format == JSON:
        url += "?format=json"

    return url


def validate_response(func):
    """
    Response is valid when `access_token` and `expires_in` are included.
    """
    @wraps(func)
    def validate(instance):
        response = func(instance)
        json_data = response.json()

        if response.status_code != requests.codes.ok:
            raise AuthorizationRejected(json_data)

        return json_data

    return validate
