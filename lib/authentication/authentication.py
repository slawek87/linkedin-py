class Authentication(object):
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        headers = {"Authorization": "Bearer " + self.token}

        return headers
