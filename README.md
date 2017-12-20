# Introduction Linkedin-py

Linkedin-py provides an easy-to-use Python interface for handle Linkedin API.

# Configuring your LinkedIn application

Before you start check how to configure your Linkedin application. To do this read the first point of this manual https://developer.linkedin.com/docs/oauth2.


# Authorization

Before we make any call to Linkedin API we have to do authorization process. Authorization process consists of two steps.

1. Login Linkedin user with special url. Linkedin-py prepares that url for you.

```python
    state = "DCEeFWf45A53sdfKef424"
    redirect_url = "https://www.example.com/auth/linkedin"
    client_id = "9996666AAAA"
    client_secret = "XYZASS"

    authorization = Authorization(
        redirect_uri=redirect_url, 
        client_id=client_id, 
        client_secret=client_secret, 
        state=state
    )

    authorization_url = authorization.get_authorization_url()

    print(authorization_url)
```
- state - A unique string value of your choice that is hard to guess. Used to prevent CSRF.
- redirect_url - The URL your users will be sent back to after authorization. This value must match one of the defined OAuth 2.0 Redirect URLs in your application configuration.
- client_id - The "API Key" value generated when you registered your application.
- secret_id - The "API Secret Key" value generated when you registered your application.

Open `authorization_url` and login in your Linkedin profile. After that you will be redirect to `redirect_url`.
In `redirect_url` you should create your own view and handle that GET request.

Linkedin API send GET request with two parameters:
- code - you need that value to get Linkedin Token.
- state - this is your CSRF. You can use this to check if request is valid.

