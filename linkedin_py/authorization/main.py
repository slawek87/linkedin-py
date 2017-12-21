import urllib
import requests
from urllib.parse import quote
from linkedin_py import const
from linkedin_py.authorization.decorators import validate_callback
from linkedin_py.utils import validate_response


class AuthorizationToken(object):
    endpoint = "https://www.linkedin.com/oauth/v2/accessToken"
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

    @validate_response
    def send_request(self):
        request_data = {
            'grant_type': self.grant_type,
            'code': self.code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        headers = {
            'Content-Type':  "application/x-www-form-urlencoded"
        }

        return requests.post(self.endpoint, data=request_data, headers=headers, timeout=60)

    def exchange_authorization_code(self):
        """
        Method returns token for given code.
        """
        response = self.send_request()

        return response.get("access_token"), response.get("expires_in")


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

    @validate_callback
    def process_callback(self, request):
        """
        Method returns access token and its expiration time.
        """
        access_token, expires_in = AuthorizationToken(
            code=request["code"],
            redirect_uri=self.redirect_uri,
            client_id=self.client_id,
            client_secret=self.client_secret
        ).exchange_authorization_code()

        return access_token, expires_in
