from rest_framework import status
from rest_framework.test import APITestCase
from coreapp.tests.utils import data_utils


class TestLoginHistoryAdminAPI(APITestCase):

    @staticmethod
    def generate_login_history_payload():
        return {
            "ip_address": "192.0.0.1",
            "user_agent": "string",
            "is_success": True,
            "otp_verification": True,
            "user": 0
        }

    def setUp(self):
        country = data_utils.create_country()
        user = data_utils.create_user(country)
        self.token = data_utils.user_token(user)

    def test_list_login_history(self):
        response = self.client.get(
            path='/api/v1/auth/admin/loginhistory/',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
