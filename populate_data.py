import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iconstruction_project.settings')
django.setup()

from inventory.models import Material, Tool, MaterialMovement
from activities.models import Project, Activity
from django.contrib.auth.models import User
from django.utils import timezone

# Crear materiales
materials_data = [
    {'name': 'Cemento', 'unit': 'kg', 'stock': 500, 'min_stock': 100},
    {'name': 'Arena', 'unit': 'm3', 'stock': 200, 'min_stock': 50},
    {'name': 'Grava', 'unit': 'm3', 'stock': 150, 'min_stock': 30},
    {'name': 'Acero', 'unit': 'kg', 'stock': 300, 'min_stock': 75},
    {'name': 'Ladrillos', 'unit': 'un', 'stock': 1000, 'min_stock': 200},
]

for data in materials_data:
    Material.objects.get_or_create(
        name=data['name'],
        defaults={
            'unit': data['unit'],
            'stock': data['stock'],
            'min_stock': data['min_stock']
        }
    )

# Crear herramientas
tools_data = [
    {'name': 'Martillo', 'code': 'HAM001', 'status': 'available'},
    {'name': 'Taladro', 'code': 'TAL001', 'status': 'available'},
    {'name': 'Sierra', 'code': 'SIE001', 'status': 'in_use'},
    {'name': 'Nivel', 'code': 'NIV001', 'status': 'available'},
    {'name': 'Cinta Métrica', 'code': 'CIN001', 'status': 'maintenance'},
]

for data in tools_data:
    Tool.objects.get_or_create(
        name=data['name'],
        code=data['code'],
        defaults={'status': data['status']}
    )

# Crear movimientos para materiales
user = User.objects.filter(is_superuser=True).first()
if user:
    for material in Material.objects.all():
        MaterialMovement.objects.get_or_create(
            material=material,
            kind='ingreso',
            quantity=50,
            user=user,
            defaults={'notes': 'Movimiento inicial de prueba'}
        )

# Crear proyectos y actividades
projects_data = [
    {'name': 'Construcción Edificio A', 'description': 'Proyecto de construcción residencial'},
    {'name': 'Remodelación Oficina', 'description': 'Remodelación de oficinas corporativas'},
]

for data in projects_data:
    project, created = Project.objects.get_or_create(
        name=data['name'],
        defaults={'description': data['description']}
    )
    if created:
        # Crear actividades para el proyecto
        activities_data = [
            {'name': 'Excavación', 'progress_percent': 100},
            {'name': 'Cimentación', 'progress_percent': 80},
            {'name': 'Estructura', 'progress_percent': 50},
        ]
        for act_data in activities_data:
            Activity.objects.get_or_create(
                project=project,
                name=act_data['name'],
                defaults={
                    'progress_percent': act_data['progress_percent'],
                    'status': 'en_progreso'
                }
            )

print("Datos de prueba agregados exitosamente.")
