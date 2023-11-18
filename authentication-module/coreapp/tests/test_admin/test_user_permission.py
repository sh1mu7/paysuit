from rest_framework import status
from rest_framework.test import APITestCase
from coreapp.tests.utils import data_utils


class TestUserPermissionAdminAPI(APITestCase):
    @staticmethod
    def generate_user_permission_payload(user, group):
        return {
            "user": user.id,
            "group": group.id
        }

    def setUp(self):
        country = data_utils.create_country()
        self.user = data_utils.create_user(country)
        self.token = data_utils.user_token(self.user)

    def test_create_user_permission(self):
        module = data_utils.create_module()
        module_permission = data_utils.create_module_permission(module)
        permission_group = data_utils.create_permission_group(module_permission)
        data = self.generate_user_permission_payload(self.user, permission_group)
        response = self.client.post(
            path='/api/v1/auth/admin/userpermission/',
            data=data, HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['data']['user'], self.user.id)

    def test_list_user_permission(self):
        response = self.client.get(
            path='/api/v1/auth/admin/userpermission/',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_permission(self):
        module = data_utils.create_module()
        module_permission = data_utils.create_module_permission(module)
        permission_group = data_utils.create_permission_group(module_permission)
        user_permission = data_utils.create_user_permission(self.user, permission_group)
        data = self.generate_user_permission_payload(self.user, permission_group)
        response = self.client.put(
            path=f'/api/v1/auth/admin/userpermission/{user_permission.id}/',
            data=data, HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['group'], permission_group.id)

    def test_delete_user_permission(self):
        module = data_utils.create_module()
        module_permission = data_utils.create_module_permission(module)
        permission_group = data_utils.create_permission_group(module_permission)
        user_permission = data_utils.create_user_permission(self.user, permission_group)
        response = self.client.delete(
            path=f'/api/v1/auth/admin/userpermission/{user_permission.id}/',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
