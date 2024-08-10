from django.db import models
from django.db.models.functions import Now
from authentication.models import CustomUser
from project.models.model1 import Package, Project
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Salary(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    package_name = models.ForeignKey(Package, on_delete=models.CASCADE)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    payroll_period = models.DateField(
        _('payroll period'), blank=True, null=True)
    _EVALUATION = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
        ("F", "F"),
    )
    _TYPE = (
        ("Insert", "Insert"),
        ("Check", "Check")
    )
    type = models.CharField(
        _('type'), choices=_TYPE, max_length=7, blank=True, null=True)
    evaluation = models.CharField(
        _('evaluation'), choices=_EVALUATION, max_length=1, blank=True, null=True)
    basic_salary = models.IntegerField(_('basic salary'), blank=True, null=True)
    bonus_fine = models.IntegerField(_('bonus/fine'), blank=True, null=True)
    final_salary = models.IntegerField(_('final salary'), blank=True, null=True)
    note = models.CharField(_('note'), blank=True, max_length=50, null=True)
        
    def __str__(self):
        return self.user.phone_no

class NotificationBase(models.Model):
    date = models.DateTimeField(_('date'), blank=True, null=True)
    title = models.CharField(_('title'),max_length=50, blank=True, null=True)
    message = models.TextField(_('message'),max_length=100, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class UserNotification(NotificationBase):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class SystemNotification(NotificationBase):
    pass