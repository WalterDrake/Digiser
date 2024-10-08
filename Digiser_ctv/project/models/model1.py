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
    type_package = models.CharField(
        _('type package'), max_length=50, choices=_TYPE, blank=True, null=True)
    total_tickets = models.IntegerField(_('total tickets'), blank=True, null=True)
    entered_tickets = models.IntegerField(_('entered tickets'), blank=True, null=True)
    not_entered_tickets = models.IntegerField(_('not entered tickets'), blank=True, null=True)
    total_real_tickets = models.IntegerField(_('total real tickets'), blank=True, null=True)
    total_fields = models.IntegerField(_('total fields'), blank=True, null=True)
    total_merging_tickets = models.IntegerField(
        _('total merging tickets'), blank=True, null=True)
    total_erroring_fields = models.IntegerField(
        _('total erroring fields'), blank=True, null=True)
    processing_check = models.IntegerField(_('processing check'), default=0)
    _PAYMENT = (
    ('Đã thanh toán', 'Đã thanh toán'),
    ('Đang xử lý', 'Đang xử lý')
)
    payment = models.CharField(
        _('payment'), max_length=30, choices=_PAYMENT, blank=True, default='Đang xử lý')

    def __str__(self):
        return self.package_name


class Package_detail(models.Model):
    package_name = models.ForeignKey(Package, on_delete=models.CASCADE)
    package_name_hash =  models.CharField(
        _('package name hash'), max_length=100, blank=True, null=True)
    inserter = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='%(class)s_inserter', blank=True, null=True)
    checker_1 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='%(class)s_checker_1', blank=True, null=True)
    checker_2 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='%(class)s_checker_2', blank=True, null=True)
    sup_name = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='%(class)s_support_name', blank=True, null=True)
    _INSERT_STATUS = (
        ('Hoàn thành nhập', 'Hoàn thành nhập'),
        ('Đang nhập', 'Đang nhập'),
        ('File lỗi', 'File lỗi'),
        ('Chưa nhập', 'Chưa nhập'),
        ('Trễ hạn nhập', 'Trễ hạn nhập')
    )
    insert_status = models.CharField(
        _('insert status'), choices=_INSERT_STATUS, max_length=16, blank=True, default='Chưa nhập')
    _CHECK_STATUS = (
        ('Hoàn thành check 1', "Hoàn thành check 1"),
        ('Hoàn thành check 2', "Hoàn thành check 2"),
        ('Sẵn sàng check', 'Sẵn sàng check'),
        ("Đang check", "Đang check"),
        ('Chưa check', 'Chưa check')
    )
    check_status_1 = models.CharField(
        _('check status 1'),choices=_CHECK_STATUS, max_length=20, blank=True, default='Chưa check')
    check_status_2 = models.CharField(
        _('check status 2'),choices=_CHECK_STATUS, max_length=20, blank=True, default='Chưa check')
    insert_url = models.CharField(
        _('package url insert'), max_length=100, blank=True, null=True)
    check_url = models.CharField(
        _('package url check'), max_length=100, blank=True, null=True)
    start_insert = models.DateField(_('started insert'), blank=True, null=True)
    dead_insert = models.DateField(_('deaded insert'), blank=True, null=True)
    finish_insert = models.DateField(
        _('finished insert'), blank=True, null=True)
    start_check = models.DateField(_('started check'), blank=True, null=True)
    dead_check = models.DateField(_('deaded check'), blank=True, null=True)
    finish_check = models.DateField(_('finished check'), blank=True, null=True)
    note_admin = models.CharField(_('note admin'), max_length=100, blank=True, null=True)
    note_check = models.CharField(_('note check'), max_length=100, blank=True, null=True)
    note_sup = models.CharField(_('note sup'), max_length=100, blank=True, null=True)
    note_insert = models.CharField(_('note insert'), max_length=100, blank=True, null=True)
    log_sup = models.DateTimeField(_('log sup'), blank=True, null=True)

    def __str__(self):
        return self.package_name.package_name
    
class Document(models.Model):
    package_name = models.ForeignKey(Package, on_delete=models.CASCADE)
    document_path = models.CharField(_('document path'), max_length=100, blank=True, null=True)
    document_name = models.CharField(_('document name'), max_length=50, blank=True, null=True)
    document_idx = models.IntegerField(_('document idx'), blank=True, null=True)
    _STATUS = (
        ('Đã nhập', 'Đã nhập'),
        ('Hoàn thành', 'Hoàn thành'),
        ('Lỗi', 'Lỗi'),
        ('Chưa check', 'Chưa check'),
        ('Chưa nhập', 'Chưa nhập'),
        ('Nhập sai', 'Nhập sai')
    )
    status_insert = models.CharField(
        _('status insert'),choices=_STATUS, max_length=30, blank=True, default='Chưa nhập')
    status_check_1 = models.CharField(
        _('status check_1'),choices=_STATUS, max_length=30, blank=True, default='Chưa check')
    status_check_2 = models.CharField(
        _('status check_2'),choices=_STATUS, max_length=30, blank=True, default='Chưa check')
    fields = models.IntegerField(_('fields'), blank=True, null=True)
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
        return self.document_name











