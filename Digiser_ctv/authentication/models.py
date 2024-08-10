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
        ('Civil, Online, A3', 'Civil, Online, A3'),
        ('Civil, Offline, A3', 'Civil, Offline, A3'),
        ('Civil, Online, A4', 'Civil, Online, A4'),
        ('Civil, Offline, A4', 'Civil, Offline, A4'),
        ('VBHC, Online, A3', 'VBHC, Online, A3'),
        ('VBHC, Offline, A3', 'VBHC, Offline, A3'),
        ('VBHC, Online, A4', 'VBHC, Online, A4'),
        ('VBHC, Offline, A4', 'VBHC, Offline, A4'),
        ('Merging, Online, A3', 'Merging, Online, A3'),
        ('Merging, Offline, A3', 'Merging, Offline, A3'),
        ('Merging, Online, A4', 'Merging, Online, A4'),
        ('Merging, Offline, A4', 'Merging, Offline, A4'),
        ('Naming, Online, A3', 'Naming, Online, A3'),
        ('Naming, Offline, A3', 'Naming, Offline, A3'),
        ('Naming, Online, A4', 'Naming, Online, A4'),
        ('Naming, Offline, A4', 'Naming, Offline, A4')
    )
    skill = models.CharField(_('skill'), max_length=30,
                             choices=_SKILLS, blank=True, null=True)
    _ROLE = (
        ("AD", "Admin"),
        ("CTV", "CTV"),
        ("MGR", "Manager"),
        ("SP", "Support"),
    )
    role = models.CharField(
        _('role'), max_length=3, choices=_ROLE, blank=True, null=True)
    updated_time = models.DateTimeField(
        _('update time'), blank=True, null=True)
    updated_user = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='updated_by')

    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['username', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_no
