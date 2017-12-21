from functools import wraps

from linkedin_py.authorization.exceptions import AuthorizationRejected


def validate_callback(func):
    """
    We need to validate two types of callback:
        - when application is rejected
        - when application is approved
    """
    from linkedin_py.authorization.main import AuthorizationCallbacks

    @wraps(func)
    def validate(instance, request):
        callback = AuthorizationCallbacks(request)

        if callback.is_rejected():
            raise AuthorizationRejected(
                {"error": callback.response["error"], "description": callback.response["error_description"]})

        if not callback.is_authenticated(instance.state):
            raise AuthorizationRejected("Authorization code is incorrect.")

        if callback.is_approved():
            return func(instance, request)

    return validate
