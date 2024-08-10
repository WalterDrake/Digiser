from django.contrib import admin
from .models import Salary, UserNotification, SystemNotification
# Register your models here.
admin.site.register([Salary, UserNotification, SystemNotification])