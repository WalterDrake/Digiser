from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LOGIN, name='login'),
    path('logout/', views.LOGOUT, name='logout'),
]