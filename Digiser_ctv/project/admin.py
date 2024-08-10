from django.contrib import admin
from .models.model1 import Project, Package, Package_detail, Document
from .models.model2 import Birth_Certificate_Document
# Register your models here.
admin.site.register([Project, Package, Package_detail, Document, Birth_Certificate_Document])