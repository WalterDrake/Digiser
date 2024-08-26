from django.urls import path
from . import views

urlpatterns = [
    path('insert/birth_certificate_document/', views.create_birth_certificate_document, name="insert_birth_certificate_document"),
]