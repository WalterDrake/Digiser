from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout')
]