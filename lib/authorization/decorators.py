from functools import wraps

from lib.authorization.exceptions import AuthorizationRejected


def validate_callback(func):
    """
    We need to validate two types of callback:
        - when application is rejected
        - when application is approved
    """
    from lib.authorization.authorization import AuthorizationCallbacks

    @wraps(func)
    def validate(instance, response):
        callback = AuthorizationCallbacks(response)

        if callback.is_rejected():
            raise AuthorizationRejected(
                {"error": callback.response["error"], "description": callback.response["error_description"]})

        if not callback.is_authenticated(instance.state):
            raise AuthorizationRejected("Authorization code is incorrect.")

        if callback.is_approved():
            return func(instance, response)

    return validate


def validate_response(func):
    """
    Response is valid when `access_token` and `expires_in` are included.
    """
    @wraps(func)
    def validate(instance):
        response = func(instance)
        json_data = response.json()

        if response.status_code == 400:
            raise AuthorizationRejected(json_data.get('error_description'))

        return json_data

    return validate
