from rest_framework import status
from rest_framework.test import APITestCase
from coreapp.tests.utils import data_utils


class TestCountryAdminAPI(APITestCase):
    @staticmethod
    def generate_country_payload():
        return {
            'name': 'Test Country',
            'code': 'Test-123',
            'phone_code': '+00',
            'flag': 'flag_url',
            'is_active': True
        }

    def setUp(self):
        country = data_utils.create_country()
        user = data_utils.create_user(country)
        self.token = data_utils.user_token(user)

    def test_create_country(self):
        response = self.client.post(
            path='/api/v1/auth/admin/country/', data=self.generate_country_payload(),
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['data']['code'], 'Test-123')

    def test_list_country(self):
        response = self.client.get(
            path='/api/v1/auth/admin/country/',
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_country(self):
        country = data_utils.create_country()
        data = self.generate_country_payload()
        data['code'] = 'Test-456'
        response = self.client.put(
            path=f"/api/v1/auth/admin/country/{country.id}/", data=data,
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['code'], 'Test-456')

    def test_delete_country(self):
        country = data_utils.create_country()
        response = self.client.delete(
            path=f"/api/v1/auth/admin/country/{country.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
