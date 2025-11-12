from django.urls import path
from . import views
urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('inventory/csv/', views.inventory_csv, name='inventory_csv'),
    path('activities/csv/', views.activities_csv, name='activities_csv'),
]
