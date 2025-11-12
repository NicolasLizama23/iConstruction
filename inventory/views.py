from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Material, MaterialMovement, Tool, ToolAssignment
from .forms import MaterialForm, MaterialMovementForm, ToolForm, ToolAssignmentForm

@login_required
def material_list(request):
    qs = Material.objects.all().order_by('name')
    return render(request, 'inventory/material_list.html', {'materials': qs})

@login_required
def material_create(request):
    form = MaterialForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Material creado.')
        return redirect('material_list')
    return render(request, 'inventory/material_form.html', {'form': form})

@login_required
def movement_create(request):
    form = MaterialMovementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        mov = form.save(commit=False)
        mov.user = request.user
        mov.save()
        # update stock
        if mov.kind == 'ingreso':
            mov.material.stock += mov.quantity
        else:
            mov.material.stock -= mov.quantity
        mov.material.save()
        messages.success(request, 'Movimiento registrado.')
        return redirect('material_list')
    return render(request, 'inventory/movement_form.html', {'form': form})

@login_required
def tool_list(request):
    return render(request, 'inventory/tool_list.html', {
        'tools': Tool.objects.all().order_by('code'),
        'assignments': ToolAssignment.objects.select_related('tool','user').order_by('-assigned_at')[:20],
    })

@login_required
def tool_create(request):
    form = ToolForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Herramienta agregada.')
        return redirect('tool_list')
    return render(request, 'inventory/tool_form.html', {'form': form})

@login_required
def tool_assign(request):
    form = ToolAssignmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        assign = form.save()
        tool = assign.tool
        tool.status = 'asignada'
        tool.assigned_to = assign.user
        tool.save()
        messages.success(request, 'Herramienta asignada.')
        return redirect('tool_list')
    return render(request, 'inventory/tool_assign_form.html', {'form': form})

@login_required
def tool_return(request, assign_id):
    assign = get_object_or_404(ToolAssignment, id=assign_id)
    assign.returned_at = assign.returned_at or __import__('datetime').datetime.now()
    assign.save()
    tool = assign.tool
    tool.status = 'disponible'
    tool.assigned_to = None
    tool.save()
    messages.success(request, 'Herramienta devuelta.')
    return redirect('tool_list')
