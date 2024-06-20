from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/upload', views.upload_import, name='import_upload'),
    path('check/', views.check, name='check'),
    path('insert/', views.insert, name='insert'),
    path('support/', views.support, name='support'),
    path('system/', views.system, name='system'),
    path('wiki/', views.wiki, name='wiki'),
    path('courses/', views.courses, name='courses'),
    path('info/',views.info, name='info'),
]
