from django.urls import path
from . import views
urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('inventory/csv/', views.inventory_csv, name='inventory_csv'),
    path('inventory/excel/', views.inventory_excel, name='inventory_excel'),
    path('activities/csv/', views.activities_csv, name='activities_csv'),
    path('activities/excel/', views.activities_excel, name='activities_excel'),
]
