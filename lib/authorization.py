import json
from urllib.request import Request, urlopen

from lib import const


class AuthorizationRejected(Exception):
    pass


class AuthenticationRejected(Exception):
    pass


class AuthorizationTokenForbidden(Exception):
    pass


class AuthorizationToken(object):
    access_token_url_template = \
        "{endpoint}/grand_type={grand_type}&code={code}&redirect_uri={redirect_uri}&client_id={client_id}&client_secret={client_secret}"

    endpoint = "https://www.linkedin.com/oauth/v2/accessToken"
    method = const.POST
    grant_type = "authorization_code"

    redirect_uri = None
    client_id = None
    client_secret = None

    def __init__(self, code):
        self.code = code

    def exchange_authorization_code(self):
        """
        Method returns token for given code.
        """
        access_token_url = self.access_token_url_template.format(
            endpoint=self.endpoint,
            grand_type=self.grant_type,
            code=self.code,
            redirect_uri=self.redirect_uri,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        request = Request(access_token_url)
        response = json.load(urlopen(request).read().decode())

        if not self.is_valid(response):
            raise AuthorizationTokenForbidden()

        return response.get("access_token"), response.get("expires_in")

    def is_valid(self, response):
        """
        Response is valid when `access_token` and `expires_in` are included.
        """
        return response.get("access_token", False) and response.get("expires_in")
    

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
        return state == self.response.state


class Authorization(object):
    """
    Class handles authorization url and authorization callback.

    * `get_authorization_url` - should be used to generate correct authorization link.
    * `process_callback` - should be used in endpoint where you handle Linkedin callbacks.
       Method returns error or user token.
    """
    authorization_url_template = \
        "{endpoint}/response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&state={state]&scope={scope}"

    endpoint = "https://www.linkedin.com/oauth/v2/authorization"
    method = const.GET
    response_type = "code"

    redirect_uri = None
    client_id = None
    scope = None
    state = None

    def __init__(self, redirect_uri, client_id, scope="r_basicprofile"):
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.scope = scope

    def get_authorization_url(self):
        """Method generates authorization url."""
        return self.authorization_url_template.format(
            endpoint=self.endpoint,
            response_type=self.response_type,
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            state=self.state,
            scope=self.scope
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
            access_token, expires_in = AuthorizationToken(response["code"])

        return access_token, expires_in
