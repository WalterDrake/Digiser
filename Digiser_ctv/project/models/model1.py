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
    type_package = models.CharField(
        _('type package'), max_length=50, choices=_TYPE, blank=True, null=True)
    total_votes = models.IntegerField(_('total votes'), blank=True, null=True)
    entered_votes = models.IntegerField(_('entered votes'), blank=True, null=True)
    not_entered_votes = models.IntegerField(_('not entered votes'), blank=True, null=True)
    total_real_votes = models.IntegerField(_('total real votes'), blank=True, null=True)
    total_fields = models.IntegerField(_('total fields'), blank=True, null=True)
    total_merging_votes = models.IntegerField(
        _('total merging votes'), blank=True, null=True)
    total_erroring_fields = models.IntegerField(
        _('total erroring fields'), blank=True, null=True)
    processing_check = models.IntegerField(_('processing check'), default=0)
    _PAYMENT = (
        ('Paid', 'Paid'),
        ('Processing', 'Processing')
    )
    payment = models.CharField(
        _('payment'), max_length=30, choices=_PAYMENT, blank=True, null=True)

    def __str__(self):
        return self.package_name


class Package_detail(models.Model):
    package_name = models.ForeignKey(Package, on_delete=models.CASCADE)
    inserter = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='%(class)s_inserter', blank=True, null=True)
    checker = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='%(class)s_checker', blank=True, null=True)
    sup_name = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='%(class)s_support_name', blank=True, null=True)
    _INSERT_STATUS = (
        ('Completed', "Completed"),
        ('Entering', "Entering"),
        ('Error', "Error"),

    )
    insert_status = models.CharField(
        _('insert status'), choices=_INSERT_STATUS, max_length=12, blank=True, null=True)
    _CHECK_STATUS = (
        ('Completed', "Completed"),
    )
    check_status = models.CharField(
        _('check status'),choices=_CHECK_STATUS, max_length=30, blank=True, null=True)
    insert_url = models.CharField(
        _('package url'), max_length=100, blank=True, null=True)
    check_url = models.CharField(
        _('package url'), max_length=100, blank=True, null=True)
    start_insert = models.DateField(_('started insert'), blank=True, null=True)
    dead_insert = models.DateField(_('deaded insert'), blank=True, null=True)
    finish_insert = models.DateField(
        _('finished insert'), blank=True, null=True)
    start_check = models.DateField(_('started check'), blank=True, null=True)
    dead_check = models.DateField(_('deaded check'), blank=True, null=True)
    finish_check = models.DateField(_('finished check'), blank=True, null=True)
    note_admin = models.CharField(_('note admin'), max_length=50, blank=True, null=True)
    note_check = models.CharField(_('note check'), max_length=50, blank=True, null=True)
    note_sup = models.CharField(_('note sup'), max_length=50, blank=True, null=True)
    log_sup = models.DateTimeField(_('log sup'), blank=True, null=True)

    def __str__(self):
        return self.package_name.package_name
    
class Document(models.Model):
    package_name = models.ForeignKey(Package, on_delete=models.CASCADE)
    document_path = models.CharField(_('document path'), max_length=50, blank=True, null=True)
    _STATUS = (
        ('Entered', 'Entered'),
        ('Completed', "Completed"),
        ('Error', "Error"),
        ('Not Checked', 'Not Checked'),
        ('Not Entered', 'Not Entered'),
        ('Incorrect Entry', 'Incorrect Entry')
    )
    status = models.CharField(
        _('status'),choices=_STATUS, max_length=30, blank=True, null=True)
    fields = models.IntegerField(_('fields'), blank=True, null=True)
    executor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='%(class)s_executor', blank=True, null=True)
    errors = models.IntegerField(
        _('errors'), blank=True, null=True)
    
    _TYPE = (
    ('KH', 'KH'),
    ('KS', 'KS'),
    ('KT', 'KT'),
    ('HN', 'HN'),
    ('CMC', 'CMC')
    )
    type = models.CharField(
        _('type'),choices=_TYPE, max_length=4, blank=True, null=True)
    
    def __str__(self):
        return self.document_path











