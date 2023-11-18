from rest_framework import status
from rest_framework.test import APITestCase
from coreapp.tests.utils import data_utils


class TestPermissionGroupAdminAPI(APITestCase):
    @staticmethod
    def generate_permission_group_payload():
        return {
            "name": "test Permission Group",
            "is_active": True,
        }

    def setUp(self):
        country = data_utils.create_country()
        user = data_utils.create_user(country)
        self.token = data_utils.user_token(user)

    def test_create_permission_group(self):
        module = data_utils.create_module()
        permission = data_utils.create_module_permission(module)
        data = self.generate_permission_group_payload()
        data['permissions'] = [permission.id]
        response = self.client.post(
            path='/api/v1/auth/admin/permissiongroup/', data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(permission.id, response.json()['data']['permissions'])

    def test_list_permission_group(self):
        response = self.client.get(
            path='/api/v1/auth/admin/permissiongroup/', data=self.generate_permission_group_payload(),
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_permission_group(self):
        module = data_utils.create_module()
        module_permission = data_utils.create_module_permission(module=module)
        permission_group = data_utils.create_permission_group(module_permission)
        data = self.generate_permission_group_payload()
        data['name'] = 'updated_name'
        data['permissions'] = [module_permission.id]
        response = self.client.put(
            path=f'/api/v1/auth/admin/permissiongroup/{permission_group.id}/', data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['name'], 'updated_name')

    def test_delete_permission_group(self):
        module = data_utils.create_module()
        module_permission = data_utils.create_module_permission(module)
        permission_group = data_utils.create_permission_group(module_permission)
        response = self.client.delete(
            path=f'/api/v1/auth/admin/permissiongroup/{permission_group.id}/',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
