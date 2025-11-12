from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('dashboard/', include('core.urls')),
    path('inventory/', include('inventory.urls')),
    path('activities/', include('activities.urls')),
    path('reports/', include('reports.urls')),
]
