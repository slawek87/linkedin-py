import unittest
from unittest.mock import Mock, patch

import requests

from linkedin_py.authorization.exceptions import AuthorizationRejected
from linkedin_py.authorization.main import Authorization
from linkedin_py.endpoints.main import retrieve_profile_data, retrieve_data


class TestLinkedIn(unittest.TestCase):
    def setUp(self):
        self.state = "DCEeFWf45A53sdfKef424"
        redirect_url = "https://www.example.com/auth/linkedin"
        client_id = "9996666AAAA"
        client_secret = "XYZASS"

        self.authorization = Authorization(
            redirect_uri=redirect_url,
            client_id=client_id,
            client_secret=client_secret,
            state=self.state
        )

    def test_get_authorization_url(self):
        authorization_url = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=9996666AAAA&redirect_uri=https%3A%2F%2Fwww.example.com%2Fauth%2Flinkedin&state=DCEeFWf45A53sdfKef424&scope=r_basicprofile"
        self.assertTrue(self.authorization.get_authorization_url(), authorization_url)

    @patch.object(requests, 'post', autospec=True)
    def test_process_callback(self, post_mock):
        mock_token = "AQUpBbh2h2cBV79XaDuI7BX7adhiCBsGZbJAk9U-NiVajfoXyY5Vg5evEByHd5XrTKXB87YjNZVfXqVJ8O0zD8kHJ_mTglttKNt4FmVxqo8yw_6ZSSn9kW8m2-rM4PAM7saq53TUc0EIFgmRo1l2DEhzSwXPcasLXTk2pCrW1u4cWoPxBo4BKaCL-iG4eIqZSMvgjjDJF-1wVttpFtU8NdrKMzSBcxJZ_jZMy98r7_WMw-Gusaz12ocjfJyhOHID5PVHJW0w9Wi40WJsXZ1iHw_Tlk2olrvew5Q6R7HFjW53yFLBvkafMRdpV4mI6n-92tq_hCHzQCgHUAqfZXnN-GG7Wz5hUw"
        mock_expires_in = 5183999
        json_mock = Mock()
        json_mock.return_value = {
            "access_token": mock_token,
            "expires_in": mock_expires_in
        }
        response_mock = Mock()
        response_mock.json = json_mock
        response_mock.status_code = 200
        response_mock.content = b'{"access_token":"AQUpBbh2h2cBV79XaDuI7BX7adhiCBsGZbJAk9U-NiVajfoXyY5Vg5evEByHd5XrTKXB87YjNZVfXqVJ8O0zD8kHJ_mTglttKNt4FmVxqo8yw_6ZSSn9kW8m2-rM4PAM7saq53TUc0EIFgmRo1l2DEhzSwXPcasLXTk2pCrW1u4cWoPxBo4BKaCL-iG4eIqZSMvgjjDJF-1wVttpFtU8NdrKMzSBcxJZ_jZMy98r7_WMw-Gusaz12ocjfJyhOHID5PVHJW0w9Wi40WJsXZ1iHw_Tlk2olrvew5Q6R7HFjW53yFLBvkafMRdpV4mI6n-92tq_hCHzQCgHUAqfZXnN-GG7Wz5hUw","expires_in":5183999}'

        post_mock.return_value = response_mock

        linkedin_received_request = {
            'code': "L3g7vIst8EW3t9PdQN6HwxS2X9fZyaUKCJQJ8hzdRtDBn6",
            'state': self.state
        }

        token, expires_in = self.authorization.process_callback(linkedin_received_request)

        self.assertTrue(token, mock_token)
        self.assertTrue(expires_in, mock_expires_in)

    def test_process_callback_fails(self):
        linkedin_received_request = {
            'code': "L3g7vIst8EW3t9PdQN6HwxS2X9fZyaUKCJQJ8hzdRtDBn6",
            'state': self.state
        }
        with self.assertRaises(AuthorizationRejected) as context:
            self.authorization.process_callback(linkedin_received_request)

        self.assertTrue('400' in str(context.exception))

    @patch.object(requests, 'get', autospec=True)
    def test_retrieve_profile_data(self, post_mock):
        response = {'firstName': 'Mathew', 'headline': 'Python Developer', 'id': 'i-Y-kHAZZz', 'industry': 'Internet', 'lastName': 'Gardner', 'positions': {'_total': 1, 'values': [{'company': {'id': 32401331, 'industry': 'Information Technology & Services', 'name': 'The MyCompany', 'size': '11-50', 'type': 'Public Company'}, 'id': 79102133391, 'isCurrent': True, 'startDate': {'month': 10, 'year': 2015}, 'title': 'Python Developer'}]}}
        access_token = "123213"
        json_mock = Mock()
        json_mock.return_value = response

        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = b'{\n  "firstName": "Mathew",\n  "headline": "Python Developer",\n  "id": "i-Y-kHAZZz",\n  "industry": "Internet",\n  "lastName": "Gardner",\n  "positions": {\n    "_total": 1,\n    "values": [{\n      "company": {\n        "id": 32401331,\n        "industry": "Information Technology & Services",\n        "name": "The MyCompany",\n        "size": "11-50",\n        "type": "Public Company"\n      },\n      "id": 79102133391,\n      "isCurrent": true,\n      "startDate": {\n        "month": 10,\n        "year": 2015\n      },\n      "title": "Python Developer"\n    }]\n  }\n}'
        response_mock.json = json_mock

        post_mock.return_value = response_mock

        self.assertTrue(retrieve_profile_data(access_token), response)

    @patch.object(requests, 'get', autospec=True)
    def test_retrieve_data(self, post_mock):
        response = {'firstName': 'Mathew', 'headline': 'Python Developer', 'lastName': 'Gardner'}
        access_token = "123213"
        json_mock = Mock()
        json_mock.return_value = response

        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = b'{\n  "firstName": "Mathew",\n  "headline": "Python Developer",\n  "lastName": "Gardner"\n}'
        response_mock.json = json_mock

        post_mock.return_value = response_mock

        url = 'https://api.linkedin.com/v1/people/~'
        params = ':(first-name,last-name,headline,picture-url)'

        self.assertTrue(retrieve_data(url=url, token=access_token, params=params), response)


if __name__ == '__main__':
    unittest.main()
