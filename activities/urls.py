from django.urls import path
from . import views
urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('projects/new/', views.project_create, name='project_create'),
    path('activities/new/', views.activity_create, name='activity_create'),
    path('logs/new/', views.activity_log_create, name='activity_log_create'),
]
