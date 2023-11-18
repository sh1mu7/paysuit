from rest_framework import status
from rest_framework.test import APITestCase
from coreapp.tests.utils import data_utils


class TestModuleAdminAPI(APITestCase):
    @staticmethod
    def generate_module_payload():
        return {
            'name': 'Test Module Name',
            'secret_key': 'FGKKK*#(&))#124459840KK',
            'is_active': True
        }

    def setUp(self):
        country = data_utils.create_country()
        user = data_utils.create_user(country)
        self.token = data_utils.user_token(user)

    def test_create_module(self):
        response = self.client.post(
            path='/api/v1/auth/admin/module/', data=self.generate_module_payload(),
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['data']['secret_key'], 'FGKKK*#(&))#124459840KK')

    def test_list_module(self):
        response = self.client.get(
            path='/api/v1/auth/admin/module/',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_module(self):
        module = data_utils.create_module()
        data = self.generate_module_payload()
        data['secret_key'] = '364hjvkfuk3w'
        response = self.client.put(
            path=f'/api/v1/auth/admin/module/{module.id}/', data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['secret_key'], '364hjvkfuk3w')

    def test_delete_module(self):
        module = data_utils.create_module()
        response = self.client.delete(
            path=f'/api/v1/auth/admin/module/{module.id}/',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
