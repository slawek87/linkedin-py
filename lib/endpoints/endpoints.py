from lib.endpoints.client import LinkedinClient


def retrieve_basic_profile_data(token):
    url = "https://api.linkedin.com/v1/people/~?format=json"
    request = LinkedinClient(token, url)

    return request.retrieve()
