from functools import wraps

import re
import requests

from linkedin_py.authorization.exceptions import AuthorizationRejected

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

        if response.status_code != requests.codes.ok:
            message = {
                'status_code': response.status_code,
                'description': response.content
            }
            raise AuthorizationRejected(message)

        return response.json()

    return validate
