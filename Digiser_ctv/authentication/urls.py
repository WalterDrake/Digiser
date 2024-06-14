from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LOGIN, name='login'),
    path('', views.home, name='home'),
    path('register/', views.REGISTER, name='register'),
    path('logout/', views.LOGOUT, name='logout'),
    path('test/', views.Test, name='test')
]