from django.urls import path
from . import views

urlpatterns = [
    path('<str:id>/<int:index>', views.input_redirect, name=""),
    path('export/<str:id>', views.export_package, name=""),
]