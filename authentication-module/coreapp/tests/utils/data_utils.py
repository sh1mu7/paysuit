from faker import Faker
from rest_framework.authtoken.models import Token

from coreapp.models import Country, User, Module, UserConfirmation, ModulePermission, PermissionGroup, UserPermission
import tempfile
from PIL import Image

fake = Faker()


def load_data():
    pass


def create_country():
    country = Country.objects.create(
        name='Test Country',
        code=fake.country_code(),
        phone_code='000',
        flag='test_url',
        is_active=True
    )
    country.save()
    return country


def create_user(country):
    user = User.objects.create(
        first_name='Mr', last_name='Admin', email='admin@admin.com', mobile='+88016753135',
        dob='1996-01-01', nid_number='157361535', nid_image='nid/default.png', country=country,
        is_verified=True, is_approved=True, is_staff=True, is_superuser=True
    )
    user.set_password('Test@12345')
    user.save()
    return user


def user_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token.key


def create_module():
    module = Module.objects.create(
        name='Test Module 1',
        secret_key='TestSecretCode1100',
        is_active=True
    )
    module.save()
    return module


def create_module_permission(module):
    module_permission = ModulePermission.objects.create(
        module=module,
        code='c439afsdk',
        desc="test module permission desc",
        is_active=True

    )
    module_permission.save()
    return module_permission


def create_permission_group(module_permission):
    permission_group = PermissionGroup.objects.create(
        name='test permission',
        is_active=True
    )
    permission_group.save()
    permission_group.permissions.set([module_permission])
    return permission_group


def create_user_permission(user, permission_group):
    user_permission = UserPermission.objects.create(
        user=user,
        group=permission_group
    )
    user_permission.save()
    return user_permission


def create_temporary_image(self):
    self.tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image = Image.new('RGB', (100, 100))
    image.save(self.tmp_file.name)
    return self.tmp_file


def create_user_confirmation(user):
    user_confirmation = UserConfirmation.objects.create(
        user=user, confirmation_code='123456', ip_address='192.168.0.3', is_used=False
    )
    user_confirmation.save()
    return user_confirmation
