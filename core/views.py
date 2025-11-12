from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from inventory.models import Material, Tool, MaterialMovement
from activities.models import Project, Activity

@login_required
def dashboard(request):
    stats = {
        'materials': Material.objects.count(),
        'tools': Tool.objects.count(),
        'projects': Project.objects.count(),
        'activities': Activity.objects.count(),
        'low_stock': Material.objects.filter(stock__lte='0').count(),
    }
    recent_movs = MaterialMovement.objects.select_related('material','user').order_by('-created_at')[:10]
    return render(request, 'core/dashboard.html', {'stats': stats, 'recent_movs': recent_movs})
