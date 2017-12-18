import urllib
import requests
from functools import wraps
from urllib.parse import quote
from lib import const


class AuthorizationRejected(Exception):
    pass


class AuthenticationRejected(Exception):
    pass


class AuthorizationTokenRejected(Exception):
    pass


def validate_response(func):
    """
    Response is valid when `access_token` and `expires_in` are included.
    """
    @wraps(func)
    def validate(response):
        if not response.get("access_token", False) and response.get("expires_in"):
            raise AuthorizationTokenRejected()
        return func(response)

    return validate


class AuthorizationToken(object):
    endpoint = "https://www.linkedin.com/oauth/v2/accessToken?"
    method = const.POST
    grant_type = "authorization_code"

    redirect_uri = None
    client_id = None
    client_secret = None

    def __init__(self, code, redirect_uri, client_id, client_secret):
        self.code = code
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret

    # @validate_response
    def exchange_authorization_code(self):
        """
        Method returns token for given code.
        """
        request_data = {
            'grand_type': self.grant_type,
            'code': self.code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.get(self.endpoint, data=request_data)

        return response.content.get("access_token"), response.content.get("expires_in")


class AuthorizationCallbacks(object):
    """
    Handle authorization callbacks: rejections, approves and authentications.
    """
    def __init__(self, response):
        self.response = response

    def is_rejected(self):
        return self.response.get("error", False)

    def is_approved(self):
        return self.response.get("error", True)

    def is_authenticated(self, state):
        """State is CSRF token."""
        return state == self.response["state"]


class Authorization(object):
    """
    Class handles authorization url and authorization callback.

    * `get_authorization_url` - should be used to generate correct authorization link.
    * `process_callback` - should be used in endpoint where you handle Linkedin callbacks.
       Method returns error or user token.
    """
    endpoint = "https://www.linkedin.com/oauth/v2/authorization?"
    method = const.GET
    response_type = "code"

    redirect_uri = None
    client_id = None
    client_secret = None
    scope = None
    state = None

    def __init__(self, redirect_uri, client_id, client_secret, state, scope="r_basicprofile"):
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.state = state
        self.scope = scope

    def get_authorization_url(self):
        """Method generates authorization url."""
        return self.endpoint + urllib.parse.urlencode(
            {
                'response_type': self.response_type,
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'state': self.state,
                'scope': self.scope
            }
        )

    def process_callback(self, response):
        """
        We need to handle two types of callback:
            - when application is rejected
            - when application is approved

        If callback is authenticated and approved,
        method returns access token and its expiration time.
        """
        callback = AuthorizationCallbacks(response)
        access_token = None
        expires_in = None

        if callback.is_rejected():
            raise AuthorizationRejected(
                {"error": callback.response["error"], "description": callback.response["error_description"]})

        if not callback.is_authenticated(self.state):
            raise AuthorizationRejected("Authorization code is incorrect.")

        if callback.is_approved():
            access_token, expires_in = AuthorizationToken(
                code=response["code"],
                redirect_uri=self.redirect_uri,
                client_id=self.client_id,
                client_secret=self.client_secret
            ).exchange_authorization_code()

        return access_token, expires_in


if __name__ == '__main__':
    state = 12134
    authorization = Authorization(
        redirect_uri="http://0.0.0.0:8000/authorize/", client_id="770vfbx6zalos0", state=state, client_secret="YJK5RcXiYISsLYzz"
    )

    print(authorization.get_authorization_url())

    response = {
        'code': "AQQ8SJkVJggFqHMeejqkeCAJN7fxZhu0E5qpsZNJI8pdak_t8946EU7C32SvJv3BfhP6uX7dv3Lxo4gTeD-a5BqIBkF3lhvDDfLPid2p6R8mu9FNB4S3MZZ6zpnGm7-GzN3uucXeVa5ZyWVVPwFZH8oimlh3TA",
        'state': state
    }

    print(authorization.process_callback(response))