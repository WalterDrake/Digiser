from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name='home'),
    path('check/', views.show_data_check, name='check'),
    path('insert/', views.show_data_insert, name='insert'),
    path('system/', views.system, name='system'),
    path('wiki/', views.wiki, name='wiki'),
    path('courses/', views.courses, name='courses'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('info/', views.info, name='info'),
    path('employees/', views.statistic_human, name = "human_statistic"),
    
    
    # duong dan cua phan admin
    path('homeadmin/', views.home_admin , name="home_admin"),
    path('listctv/', views.list_ctv, name="list_ctv")
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)