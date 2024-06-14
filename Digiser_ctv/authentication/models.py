from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_no = models.CharField(_('phone number'), max_length=20, blank=True, unique=True)
    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['username','email']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_no