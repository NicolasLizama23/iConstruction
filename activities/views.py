from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project, Activity, ActivityLog
from .forms import ProjectForm, ActivityForm, ActivityLogForm

@login_required
def project_list(request):
    return render(request, 'activities/project_list.html', {'projects': Project.objects.all()})

@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Proyecto creado.')
        return redirect('project_list')
    return render(request, 'activities/project_form.html', {'form': form})

@login_required
def activity_create(request):
    form = ActivityForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Actividad creada.')
        return redirect('project_list')
    return render(request, 'activities/activity_form.html', {'form': form})

@login_required
def activity_log_create(request):
    form = ActivityLogForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Avance registrado.')
        return redirect('project_list')
    return render(request, 'activities/activity_log_form.html', {'form': form})
