from django.db import models
from django.db.models.functions import Now
from authentication.models import CustomUser
from project.models import Package, Project
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
    evaluation = models.CharField(
        _('evaluation'), choices=_EVALUATION, max_length=1, blank=True)
    basic_salary = models.IntegerField(_('basic salary'), blank=True)
    bonus_fine = models.IntegerField(_('bonus/fine'), blank=True)
    final_salary = models.IntegerField(_('final salary'), blank=True)
    note = models.CharField(_('note'), blank=True, max_length=50)
    total_votes = models.OneToOneField(
        Package, on_delete=models.CASCADE,related_name='salary_total_votes', blank=True)
    total_fields = models.OneToOneField(
        Package, on_delete=models.CASCADE,related_name='salary_total_fields', blank=True)
    total_merging_votes = models.OneToOneField(
        Package, on_delete=models.CASCADE,related_name='salary_total_merging_votes', blank=True)
    total_erroring_fields = models.OneToOneField(
        Package, on_delete=models.CASCADE,related_name='salary_total_erroring_fields', blank=True)
    processing_check = models.OneToOneField(
        Package, on_delete=models.CASCADE,related_name='salary_processing_check', blank=True)

    def __str__(self):
        return self.user.phone_no

