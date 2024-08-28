from django.contrib import admin
from .models.model1 import Project, Package, Package_detail, Document
from .models.model2 import Birth_Certificate_Document
# Register your models here.
class CustomProjectsite(admin.ModelAdmin):
    model = Project
    list_display = ('project_name', 'created',)
    search_fields = ('project_name',)
    ordering = ('created',)
class CustomPackagesite(admin.ModelAdmin):
    model = Package
    list_display = ('package_name', 'project', 'type_package','payment')
    search_fields= ('package_name',)
class CustomPackageDetailsite(admin.ModelAdmin):
    model = Package_detail
    list_display = ('package_name', 'insert_status', 'check_status_1', 'check_status_2',)
    search_fields= ('package_name__package_name',)
class CustomDocumentsite(admin.ModelAdmin):
    model = Document
    list_display = ('document_name', 'package_name', 'status_insert','status_check_1', 'status_check_2')
    search_fields= ('document_name',)
class CustomBirthCertificateDocumentsite(admin.ModelAdmin):
    model = Birth_Certificate_Document
    list_display = ('document','executor',)
    search_fields= ('document__document_path',)

admin.site.register(Birth_Certificate_Document, CustomBirthCertificateDocumentsite)
admin.site.register(Project,CustomProjectsite)
admin.site.register(Package,CustomPackagesite)
admin.site.register(Package_detail,CustomPackageDetailsite)
admin.site.register(Document,CustomDocumentsite)