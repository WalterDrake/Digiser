from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_no = models.CharField(
        _('phone number'), max_length=15, unique=True, primary_key=True)
    is_verified = models.BooleanField(_('is verified'), default=False)
    full_name = models.CharField(_('full name'), blank=True, max_length=20, null=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    address = models.CharField(_('address'), blank=True, max_length=30, null=True)
    qualification = models.CharField(
        _('qualification'), blank=True, max_length=20, null=True)
    identification = models.CharField(
        _('identification'), blank=True, max_length=15, null=True)
    identification_address = models.CharField(
        _('identification address'), blank=True, max_length=30, null=True)
    note = models.CharField(_('note'), blank=True, max_length=50, null=True)
    account_number = models.CharField(
        _('account number'), blank=True, max_length=20, null=True)
    bank_name = models.CharField(_('bank name'), max_length=20, blank=True, null=True)
    branch = models.CharField(_('branch'), max_length=20, blank=True, null=True)
    owner = models.CharField(_('owner'), max_length=20, blank=True, null=True)
    code_bank = models.CharField(_('code bank'), max_length=10, blank=True, null=True)
    code = models.CharField(
        _('code'), max_length=10, blank=True, unique=True, null=True)
    _STATUSES = (
        ("AC", "Working"),
        ("NA", "Quit"),
    )
    status = models.CharField(
        _('status'), max_length=2, choices=_STATUSES, blank=True, null=True)
    _SKILLS = (
        ('Civil Status, Online, A3', 'Civil Status, Online, A3'),
        ('Civil Status, Offline, A3', 'Civil Status, Offline, A3'),
        ('Civil Status, Online, A4', 'Civil Status, Online, A4'),
        ('Civil Status, Offline, A4', 'Civil Status, Offline, A4'),
        ('Administrative Document, Online, A3', 'Administrative Document, Online, A3'),
        ('Administrative Document, Offline, A3', 'Administrative Document, Offline, A3'),
        ('Administrative Document, Online, A4', 'Administrative Document, Online, A4'),
        ('Administrative Document, Offline, A4', 'Administrative Document, Offline, A4'),
        ('Merge, Online, A3', 'Merge, Online, A3'),
        ('Merge, Offline, A3', 'Merge, Offline, A3'),
        ('Merge, Online, A4', 'Merge, Online, A4'),
        ('Merge, Offline, A4', 'Merge, Offline, A4'),
        ('Name, Online, A3', 'Name, Online, A3'),
        ('Name, Offline, A3', 'Name, Offline, A3'),
        ('Name, Online, A4', 'Name, Online, A4'),
        ('Name, Offline, A4', 'Name, Offline, A4')
    )
    skill = models.CharField(_('skill'), max_length=50,
                             choices=_SKILLS, blank=True, null=True)
    _ROLE = (
        ("Admin", "Admin"),
        ("CTV", "CTV"),
        ("Manager", "Manager"),
        ("Support", "Support"),
    )
    role = models.CharField(
        _('role'), max_length=8, choices=_ROLE, blank=True, null=True)
    updated_time = models.DateTimeField(
        _('update time'), blank=True, null=True)
    updated_user = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_updated_user')

    USERNAME_FIELD = 'code'
    REQUIRED_FIELDS = ['username', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_no
