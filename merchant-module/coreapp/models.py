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


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model responsible for authentication and authorization
    """
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(unique=True, max_length=20)
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    token = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class BusinessCategory(BaseModel):
    name = models.CharField(max_length=100)
    is_active = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Business(BaseModel):
    """
    Business model which will be used for storing the information related to business.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)
    business_type = models.SmallIntegerField(choices=constants.BusinessType.choices)
    legal_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', default='logos/default.png')
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    bank_name = models.CharField(max_length=100)
    account_holder_name = models.CharField(max_length=100)
    account_no = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=100)

    website = models.CharField(max_length=100)
    status = models.SmallIntegerField(
        choices=constants.BusinessStatus.choices,
        default=constants.BusinessStatus.PENDING
    )

    def __str__(self):
        return self.legal_name


class BusinessDocument(BaseModel):
    """
    BusinessDocument model which will be used for KYC.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    doc_type = models.SmallIntegerField(choices=constants.LegalDocumentChoices.choices)
    doc_status = models.SmallIntegerField(
        choices=constants.DocumentStatus.choices,
        default=constants.DocumentStatus.PENDING
    )
    reject_reason = models.CharField(max_length=250, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.document.name}"

    def get_business_name(self):
        return self.business.display_name

    @cached_property
    def get_url(self):
        return f"{settings.MEDIA_HOST}{self.document.url}"


class Webhook(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    url = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.url)
