from django.contrib import admin
from .models import Project, Package, Package_detail
# Register your models here.
admin.site.register([Project, Package, Package_detail])