from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
import csv
from inventory.models import Material, Tool
from activities.models import Project, Activity

@login_required
def reports_home(request):
    return render(request, 'reports/reports_home.html')

@login_required
def inventory_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventario.csv"'
    writer = csv.writer(response)
    writer.writerow(['Material','Unidad','Stock','Stock Minimo'])
    for m in Material.objects.all():
        writer.writerow([m.name, m.unit, m.stock, m.min_stock])
    writer.writerow([])
    writer.writerow(['Herramienta','Código','Estado'])
    for t in Tool.objects.all():
        writer.writerow([t.name, t.code, t.status])
    return response

@login_required
def activities_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="actividades.csv"'
    writer = csv.writer(response)
    writer.writerow(['Proyecto','Actividad','Progreso','Estado'])
    for a in Activity.objects.select_related('project').all():
        writer.writerow([a.project.name, a.name, a.progress_percent, a.status])
    return response
