from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from coreapp.base import BaseModel


# Create your models here.
class Package(BaseModel):
    name = models.CharField(max_length=100)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    renewal_fee = models.DecimalField(max_digits=10, decimal_places=2)
    local = models.DecimalField(decimal_places=2, max_digits=10)
    international = models.DecimalField(decimal_places=2, max_digits=10)
    mfs = models.DecimalField(decimal_places=2, max_digits=10)
    desc = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Subscription(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business = models.ForeignKey('coreapp.Business', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, editable=False)
    expiry_date = models.DateTimeField()

    @cached_property
    def get_is_active(self):
        now = timezone.now()
        return now < self.expiry_date
