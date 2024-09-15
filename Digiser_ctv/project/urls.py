from django.urls import path
from . import views

urlpatterns = [
    path('<str:id>/<int:index>', views.form_redirect, name=""),
    path('export/user/', views.export_package, name=""),
    path('redirect', views.package_redirect, name=""),
]