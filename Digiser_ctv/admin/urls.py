from django.urls import path
from . import views

urlpatterns = [
    # Admin urls
    path('', views.home_admin , name="home_admin"),
    path('ctv/', views.ctv_list , name="ctv_list"),
    path('loginlog/', views.list_loginlog, name="list_loginlog"),
]
