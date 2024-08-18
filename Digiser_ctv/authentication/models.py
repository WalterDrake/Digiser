from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(_('username'), blank=True, max_length=30, null=True)
    email = models.EmailField(_('email address'), blank=True, max_length=30, null=True)
    phone_no = models.CharField(
        _('phone number'), max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(_('is verified'), default=False)
    full_name = models.CharField(_('full name'), max_length=100)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    address = models.CharField(_('address'), blank=True, max_length=100, null=True)
    qualification = models.CharField(
        _('qualification'), blank=True, max_length=20, null=True)
    identification = models.CharField(
        _('identification'), blank=True, max_length=15, null=True)
    identification_address = models.CharField(
        _('identification address'), blank=True, max_length=100, null=True)
    note = models.CharField(_('note'), blank=True, max_length=100, null=True)
    account_number = models.CharField(
        _('account number'), blank=True, max_length=20, null=True)
    bank_name = models.CharField(_('bank name'), max_length=30, blank=True, null=True)
    branch = models.CharField(_('branch'), max_length=30, blank=True, null=True)
    owner = models.CharField(_('owner'), max_length=100, blank=True, null=True)
    code_bank = models.CharField(_('code bank'), max_length=10, blank=True, null=True)
    code = models.CharField(
        _('code'), max_length=10, blank=True, unique=True, null=True)
    _STATUSES = (
    ('Đang làm', 'Đang làm'),
    ('Nghỉ việc', 'Nghỉ việc')
)
    status = models.CharField(
        _('status'), max_length=15, choices=_STATUSES, blank=True, null=True)
    _SKILLS = (
        ('Hộ tịch, Online, A3', 'Hộ tịch, Online, A3'),
        ('Hộ tịch, Offline, A3', 'Hộ tịch, Offline, A3'),
        ('Hộ tịch, Online, A4', 'Hộ tịch, Online, A4'),
        ('Hộ tịch, Offline, A4', 'Hộ tịch, Offline, A4'),
        ('VBHC, Online, A3', 'VBHC, Online, A3'),
        ('VBHC, Offline, A3', 'VBHC, Offline, A3'),
        ('VBHC, Online, A4', 'VBHC, Online, A4'),
        ('VBHC, Offline, A4', 'VBHC, Offline, A4'),
        ('Ghép, Online, A3', 'Ghép, Online, A3'),
        ('Ghép, Offline, A3', 'Ghép, Offline, A3'),
        ('Ghép, Online, A4', 'Ghép, Online, A4'),
        ('Ghép, Offline, A4', 'Ghép, Offline, A4'),
        ('Đặt tên, Online, A3', 'Đặt tên, Online, A3'),
        ('Đặt tên, Offline, A3', 'Đặt tên, Offline, A3'),
        ('Đặt tên, Online, A4', 'Đặt tên, Online, A4'),
        ('Đặt tên, Offline, A4', 'Đặt tên, Offline, A4')
    )
    skill = models.CharField(_('skill'), max_length=30,
                             choices=_SKILLS, blank=True, null=True)
    _ROLE = (
        ("Admin", "Admin"),
        ("CTV", "CTV"),
        ("Manager", "Manager"),
        ("Support", "Support"),
    )
    role = models.CharField(
        _('role'), max_length=7, choices=_ROLE, blank=True, null=True)
    updated_time = models.DateTimeField(
        _('update time'), blank=True, null=True)
    updated_user = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='updated_by')

    USERNAME_FIELD = 'code'
    REQUIRED_FIELDS = ['full_name', 'phone_no', 'username']

    objects = CustomUserManager()

    def __str__(self):
        return self.code
