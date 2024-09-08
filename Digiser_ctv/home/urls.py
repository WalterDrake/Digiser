from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('check/', views.show_data_check, name='check'),
    path('insert/', views.show_data_insert, name='insert'),
    path('support/', views.support, name='support'),
    path('system/', views.system, name='system'),
    path('wiki/', views.wiki, name='wiki'),
    path('courses/', views.courses, name='courses'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('info/', views.info, name='info'),
    path('statistic/', views.show_data_statistic, name="data_statistic"),
    path('employees/', views.statistic_human, name = "human_statistic"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)