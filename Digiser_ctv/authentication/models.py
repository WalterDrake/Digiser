from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
import datetime
# Create your models here.

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_no = models.CharField(_('phone number'), max_length=20, unique=True)
    is_verified = models.BooleanField(_('is verified'), default=False)
    full_name = models.CharField(_('full name'), blank=True, max_length=20)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    address = models.CharField(_('address'), blank=True, max_length=30)
    qualification = models.CharField(
        _('qualification'), blank=True, max_length=20)
    identification = models.CharField(
        _('identification'), blank=True, max_length=15)
    identification_address = models.CharField(
        _('identification address'), blank=True, max_length=30)
    note = models.CharField(_('note'), blank=True, max_length=50)
    account_number = models.CharField(
        _('account number'), blank=True, max_length=20)
    bank_name = models.CharField(_('bank name'), max_length=20, blank=True)
    branch = models.CharField(_('branch'), max_length=20, blank=True)
    owner = models.CharField(_('owner'), max_length=20, blank=True)
    code_bank = models.CharField(_('code bank'), max_length=10, blank=True)
    code_ctv = models.CharField(_('code ctv'), max_length=10, blank=True, unique=True)
    role = models.CharField(_('role'), max_length=10, blank=True)
    row = models.IntegerField(_('row'), blank=True, null=True)
    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['username', 'email']
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_no
