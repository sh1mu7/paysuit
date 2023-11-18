from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from rest_framework import status
from rest_framework.test import APITestCase

from coreapp.models import User, UserConfirmation
from coreapp.tests.utils import data_utils


class TestAuthPublicTestAPI(APITestCase):

    def setUp(self):
        self.country = data_utils.create_country()
        self.user = data_utils.create_user(self.country)
        self.tmp_file = data_utils.create_temporary_image(self)
        self.user_confirmation = data_utils.create_user_confirmation(self.user)
        self.token = data_utils.user_token(self.user)

    def test_list_country(self):
        response = self.client.get('/api/v1/auth/public/country/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup_with_valid_data(self):
        country = data_utils.create_country()
        payload = {
            'first_name': 'MR.',
            'last_name': 'Merchant',
            'email': 'merchant@paysuitebd.com',
            'mobile': '+8801600202020',
            'password': 'Test@1234',
            'confirm_password': 'Test@1234',
            'dob': '1996-02-23',
            'nid_number': '6357252',
            'nid_image': self.tmp_file,
            'country': country.id
        }
        response = self.client.post(
            path='/api/v1/auth/public/signup/',
            data=encode_multipart(data=payload, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_with_invalid_data(self):
        country = data_utils.create_country()
        tmp_file = data_utils.create_temporary_image(self)
        payload = {
            'first_name': 'MR.',
            'last_name': 'Merchant',
            'email': 'admin@admin.com',
            'mobile': '+8801600202020',
            'password': 'Test@1234',
            'confirm_password': 'Test@1234',
            'dob': '1996-02-23',
            'nid_number': '6357252',
            'nid_image': tmp_file,
            'country': country.id
        }
        response = self.client.post(
            path='/api/v1/auth/public/signup/',
            data=encode_multipart(data=payload, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT
        )
        self.assertNotEquals(response.status_code, status.HTTP_201_CREATED)

    def test_login_invalid_data(self):
        payload = {
            'email': self.user.email,
            'password': '1234'
        }
        response = self.client.post(
            path='/api/v1/auth/public/login/', data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_valid_data(self):
        payload = {
            'email': 'admin@admin.com',
            'password': 'Test@12345'
        }
        response = self.client.post(
            path='/api/v1/auth/public/login/', data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_2fa_with_invalid_data(self):
        payload = {
            'email': 'admin@admin.com',
            'password': 'Test@12345'
        }
        response = self.client.post(
            path='/api/v1/auth/public/login/', data=payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_confirmation = UserConfirmation.objects.last()
        payload_2fa = {
            'email': self.user.email,
            'password': 'Test@12345',
            'code': '98789'
        }

        response2 = self.client.post(
            path='/api/v1/auth/public/login/2fa/', data=payload_2fa
        )
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_2fa_with_valid_data(self):
        payload = {
            'email': 'admin@admin.com',
            'password': 'Test@12345'
        }
        response = self.client.post(
            path='/api/v1/auth/public/login/', data=payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_confirmation = UserConfirmation.objects.last()
        payload_2fa = {
            'email': self.user.email,
            'password': 'Test@12345',
            'code': user_confirmation.confirmation_code
        }

        response2 = self.client.post(
            path='/api/v1/auth/public/login/2fa/', data=payload_2fa
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        user = User.objects.create(
            first_name='Mr', last_name='Admin2', email='admin@test.com', mobile='+88017753135',
            dob='1996-02-01', nid_number='1572361535', nid_image='nid/default.png',
            country=self.country,
            is_verified=True, is_approved=True, is_staff=True, is_superuser=True
        )
        token = data_utils.user_token(user)
        response = self.client.get(path='/api/v1/auth/public/delete/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #
    def test_forgot_password_with_valid_email(self):
        payload = {
            'email': 'admin@admin.com'
        }
        response = self.client.post(path='/api/v1/auth/public/forget/password/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forgot_password_with_invalid_email(self):
        payload = {
            'email': 'fake@admin.com'
        }
        response = self.client.post(path='/api/v1/auth/public/forget/password/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_password_confirm_with_valid_data(self):
        payload = {
            'email': self.user.email
        }
        response = self.client.post(path='/api/v1/auth/public/forget/password/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_confirmation = UserConfirmation.objects.last()
        payload2 = {
            'email': self.user.email,
            'code': user_confirmation.confirmation_code,
            'password': 'Test@12345'
        }
        response2 = self.client.post(path='/api/v1/auth/public/forget/password/confirm/', data=payload2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_forgot_password_confirm_with_invalid_data(self):
        payload = {
            'email': self.user.email
        }
        response = self.client.post(path='/api/v1/auth/public/forget/password/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload2 = {
            'email': self.user.email,
            'code': 78987,
            'password': 'Test@12345'
        }
        response2 = self.client.post(path='/api/v1/auth/public/forget/password/confirm/', data=payload2)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_profile(self):
        response = self.client.get(path='/api/v1/auth/public/profile/', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_profile_with_valid_data(self):
        payload = {
            "uid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "first_name": "test first name",
            "last_name": "test last name",
            "wallet": "400",
            "otp_method": 0
        }

        response = self.client.post(
            path='/api/v1/auth/public/profile/', data=payload,
            HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_profile_with_invalid_data(self):
        payload = {
            "uid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "first_name": "test first name",
            "last_name": "test last name",
            "wallet": "400",
            "otp_method": 12
        }

        response = self.client.post(
            path='/api/v1/auth/public/profile/', data=payload,
            HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verification_check_with_valid_code(self):
        payload = {
            'email': self.user.email,
            'code': self.user_confirmation.confirmation_code
        }

        response = self.client.post(
            path='/api/v1/auth/public/verification/check/', data=payload,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verification_check_with_invalid_code(self):
        payload = {
            'email': self.user.email,
            'code': '12345'
        }

        response = self.client.post(
            path='/api/v1/auth/public/verification/check/', data=payload,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verification_resend_with_valid_email(self):
        payload = {
            'email': self.user.email
        }
        response = self.client.post(path='/api/v1/auth/public/verification/resend/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verification_resend_with_invalid_email(self):
        payload = {
            'email': '01735677848'
        }
        response = self.client.post(path='/api/v1/auth/public/verification/resend/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_2fa_setup_get_auth_url(self):
        response = self.client.get(path='/api/v1/auth/public/setup/2fa/', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_2fa_setup_otp_key(self):
        response = self.client.post(path='/api/v1/auth/public/setup/2fa/', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
