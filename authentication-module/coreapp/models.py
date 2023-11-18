import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from coreapp import constants
from coreapp.manager import MyUserManager
from .base import BaseModel
from .utils import totp_utils


# Create your models here.

class Country(BaseModel):
    """
    Country model responsible country dropdown
    """
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    phone_code = models.CharField(_("Phone code"), max_length=50)
    flag = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model responsible for authentication and authorization
    """
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(unique=True, max_length=20)
    dob = models.DateField()
    image = models.ImageField(upload_to='users/', default='users/default.png')
    nid_number = models.CharField(max_length=20)
    nid_image = models.ImageField(upload_to='nid/')
    gender = models.SmallIntegerField(choices=constants.GenderChoices.choices, default=constants.GenderChoices.MALE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    otp_key = models.CharField(max_length=100, default=uuid.uuid4, editable=False)
    otp_method = models.SmallIntegerField(choices=constants.OTPMethod.choices, default=constants.OTPMethod.EMAIL)
    fcm_key = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @cached_property
    def get_image_url(self):
        return self.image.url if self.image else None

    @cached_property
    def get_country_name(self):
        return self.country.name

    @cached_property
    def get_google_authenticator_url(self):
        return totp_utils.generate_google_auth_key(self)


class UserConfirmation(BaseModel):
    """
    User confirmation model for generating OTP Codes
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.confirmation_code} : {self.is_used}"


class LoginHistory(BaseModel):
    """
    Login History model which stores the IP and other information related to authentication
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=500)
    is_success = models.BooleanField(default=False)
    otp_verification = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.ip_address} - {self.user_agent} - {self.is_success}"


class Document(BaseModel):
    """
    Document model which is used for centralized file upload
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    doc_type = models.SmallIntegerField(choices=constants.DocumentChoices.choices)

    def __str__(self):
        return f"{self.owner} - {self.document.name}"

    @cached_property
    def get_url(self):
        return f"{settings.MEDIA_HOST}{self.document.url}"


class Module(BaseModel):
    name = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def generate_secret_key(self):
        self.secret_key = str(uuid.uuid4())
        self.save()


class ModulePermission(BaseModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['module', 'code'], name='unique_permission_code')
        ]


class PermissionGroup(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(ModulePermission)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserPermission(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(PermissionGroup, on_delete=models.CASCADE)
