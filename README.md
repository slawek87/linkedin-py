# Introduction Linkedin-py

Linkedin-py provides an easy-to-use Python interface for handle Linkedin API.

# Configuring your LinkedIn application

Before you start check how to configure your Linkedin application. To do this read the first point of this manual https://developer.linkedin.com/docs/oauth2.


# Authorization Request

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

Linkedin API sends GET request with two parameters:
- code - you need that value to get Linkedin Token.
- state - this is your CSRF. You can use this to check if request is valid.

2. Process callback.
When you got `code` you need to exchange it to get token.

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

    linkedin_received_request = {
        'code': "L3g7vIst8EW3t9PdQN6HwxS2X9fZyaUKCJQJ8hzdRtDBn6",
        'state': state
    }

    access_token, expires_in = authorization.process_callback(linkedin_received_request)
```

Method `process_callback` returns two values:
   - Linkedin Token needed to authenticate user's requests.
   - Linkedin Token's expiration time.


# Linkedin Requests

Here you will find list of implemented Linkedin Requests.

## Profile Data

In default request returns response with whole profile data.

```python
    token = 'AQVUFKfVWHbIBn9ckq_TjJMlFBw'
    profile_data = retrieve_profile_data(token)

    print(profile_data)
```

You can modify it by setting up your own param value.

```python
    token = 'AQVUFKfVWHbIBn9ckq_TjJMlFBw'
    params = ':(first-name,last-name,headline,picture-url)'
    profile_data = retrieve_profile_data(token)

    print(profile_data)
```

This request returns response only with `firstName', 'headline', 'lastName', pictureUrl`.

* Request doesn't return missing data in your profile.
