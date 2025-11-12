from django.urls import path
from . import views
urlpatterns = [
    path('', views.material_list, name='material_list'),
    path('materials/new/', views.material_create, name='material_create'),
    path('movements/new/', views.movement_create, name='movement_create'),
    path('tools/', views.tool_list, name='tool_list'),
    path('tools/new/', views.tool_create, name='tool_create'),
    path('tools/assign/', views.tool_assign, name='tool_assign'),
    path('tools/return/<int:assign_id>/', views.tool_return, name='tool_return'),
]
