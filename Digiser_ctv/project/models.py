from django.db import models
from authentication.models import CustomUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Project(models.Model):
    project_name = models.CharField(
        _('project name'), max_length=20, blank=True, unique=True, primary_key=True)
    project_description = models.CharField(
        _('project description'), max_length=100, blank=True)
    code_customer = models.CharField(
        _('code customer'), max_length=5, blank=True)
    created = models.DateField(_('created'))

    def __str__(self):
        return self.project_name


class Package(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    package_name = models.CharField(
        _('package name'), max_length=100, blank=True, unique=True, primary_key=True)
    _TYPE = (
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
    type_package = models.CharField(
        _('type package'), max_length=30, choices=_TYPE, blank=True)
    note_admin = models.CharField(_('note admin'), max_length=50, blank=True)
    total_votes = models.IntegerField(_('total votes'), blank=True)
    total_real_votes = models.IntegerField(_('total real votes'), blank=True)
    total_fields = models.IntegerField(_('total fields'), blank=True)
    total_merging_votes = models.IntegerField(
        _('total merging votes'), blank=True)
    total_erroring_fields = models.IntegerField(
        _('total error fields'), blank=True)
    processing_check = models.IntegerField(_('processing check'), default=0)

    def __str__(self):
        return self.package_name


class Package_detail(models.Model):
    package_name = models.ForeignKey(Package, on_delete=models.CASCADE)
    inserter = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,related_name='inserter', blank=True)
    checker = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,related_name='checker', blank=True)
    sup_name = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,related_name='support_name', blank=True)
    insert_status = models.CharField(
        _('insert status'), max_length=10, blank=True)
    check_status = models.CharField(
        _('check status'), max_length=10, blank=True)
    insert_url = models.CharField(
        _('package url'), max_length=100, blank=True)
    check_url = models.CharField(
        _('package url'), max_length=100, blank=True)
    start_insert = models.DateField(_('started insert'), blank=True, null=True)
    dead_insert = models.DateField(_('deaded insert'), blank=True, null=True)
    finish_insert = models.DateField(
        _('finished insert'), blank=True, null=True)
    status_insert = models.CharField(
        _('status insert'), max_length=50, blank=True)
    start_check = models.DateField(_('started check'), blank=True, null=True)
    dead_check = models.DateField(_('deaded check'), blank=True, null=True)
    finish_check = models.DateField(_('finished check'), blank=True, null=True)
    status_check = models.DateField(_('status check'), blank=True, null=True)
    note_check = models.CharField(_('note check'), max_length=50, blank=True)
    note_sup = models.CharField(_('note sup'), max_length=50, blank=True)
    log_sup = models.DateTimeField(_('log sup'), blank=True)

    def __str__(self):
        return self.package_name