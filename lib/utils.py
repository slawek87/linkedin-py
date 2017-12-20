from functools import wraps

import requests

from lib.authorization.exceptions import AuthorizationRejected


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
