from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('check/', views.check, name='check'),
    path('insert/', views.insert, name='insert'),
    path('support/', views.support, name='support'),
    path('system/', views.system, name='system'),
    path('wiki/', views.wiki, name='wiki'),
    path('courses/', views.courses, name='courses'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('info/', views.info, name='info'),
    path('statistic/', views.show_data_statistic, name="data_statistic"),
    path('employees/', views.statistic_human, name = "human_statistic")
]
