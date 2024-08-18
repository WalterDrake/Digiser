from django.contrib import admin
from .models import Salary, UserNotification, SystemNotification
# Register your models here.
class CustomSalarysite(admin.ModelAdmin):
    model = Salary
    list_display = ('package_name', 'project_name', 'type', 'user',)
    search_fields = ('type','package_name__package_name','user__full_name')
    list_filter = ('user__full_name',)
admin.site.register(Salary, CustomSalarysite)
admin.site.register(UserNotification)
admin.site.register(SystemNotification)