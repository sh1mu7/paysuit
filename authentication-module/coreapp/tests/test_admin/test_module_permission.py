from rest_framework import status
from rest_framework.test import APITestCase
from coreapp.tests.utils import data_utils


class TestModulePermissionAdminAPI(APITestCase):
    @staticmethod
    def generate_module_permission_payload():
        return {
            "code": "c439afsdk",
            "desc": "string",
            "is_active": True,
        }

    def setUp(self):
        country = data_utils.create_country()
        user = data_utils.create_user(country)
        self.token = data_utils.user_token(user)

    def test_create_module_permission(self):
        module = data_utils.create_module()
        data = self.generate_module_permission_payload()
        data['module'] = module.id
        response = self.client.post(
            path='/api/v1/auth/admin/modulepermission/', data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['data']['module'], module.id)

    def test_list_module_permission(self):
        response = self.client.get(
            path='/api/v1/auth/admin/modulepermission/',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_module_permission(self):
        module = data_utils.create_module()
        module_permission = data_utils.create_module_permission(module=module)
        data = self.generate_module_permission_payload()
        data['code'] = 'test'
        data['module'] = module.id
        response = self.client.put(
            path=f'/api/v1/auth/admin/modulepermission/{module_permission.id}/', data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['code'], 'test')

    def test_delete_module_permission(self):
        module = data_utils.create_module()
        module_permission = data_utils.create_module_permission(module)
        response = self.client.delete(
            path=f'/api/v1/auth/admin/modulepermission/{module_permission.id}/',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
