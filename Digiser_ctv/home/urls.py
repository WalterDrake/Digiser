from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('check/', views.show_data_check, name='check'),
    path('insert/', views.show_data_insert, name='insert'),
    path('system/', views.system, name='system'),
    path('wiki/', views.wiki, name='wiki'),
    path('courses/', views.courses, name='courses'),
    path('info/', views.info, name='info'),
]
