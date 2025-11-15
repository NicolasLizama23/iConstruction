import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iconstruction_project.settings')
django.setup()

from inventory.models import Material, Tool, MaterialMovement, ToolAssignment
from activities.models import Project, Activity
from django.contrib.auth.models import User
from django.utils import timezone
import random

# Crear materiales (200+ para pruebas de rendimiento)
materials_data = []
for i in range(1, 251):  # 250 materiales
    materials_data.append({
        'name': f'Material {i}',
        'unit': random.choice(['kg', 'm3', 'un', 'lt']),
        'stock': random.randint(100, 1000),
        'min_stock': random.randint(10, 100)
    })

for data in materials_data:
    Material.objects.get_or_create(
        name=data['name'],
        defaults={
            'unit': data['unit'],
            'stock': data['stock'],
            'min_stock': data['min_stock']
        }
    )

# Crear herramientas (más herramientas para pruebas)
tools_data = []
for i in range(1, 51):  # 50 herramientas
    tools_data.append({
        'name': f'Herramienta {i}',
        'code': f'HER{i:03d}',
        'status': random.choice(['disponible', 'asignada', 'mantenimiento'])
    })

for data in tools_data:
    Tool.objects.get_or_create(
        name=data['name'],
        code=data['code'],
        defaults={'status': data['status']}
    )

# Crear movimientos para materiales (muchos movimientos para pruebas)
user = User.objects.filter(is_superuser=True).first()
if user:
    materials = list(Material.objects.all())
    for i in range(1000):  # 1000 movimientos
        material = random.choice(materials)
        MaterialMovement.objects.get_or_create(
            material=material,
            kind=random.choice(['ingreso', 'salida']),
            quantity=random.randint(1, 100),
            user=user,
            defaults={'notes': f'Movimiento de prueba {i+1}'}
        )

# Crear asignaciones de herramientas
users = list(User.objects.all())
tools = list(Tool.objects.filter(status='asignada'))
for i, tool in enumerate(tools[:20]):  # Asignar 20 herramientas
    if users:
        assigned_user = random.choice(users)
        ToolAssignment.objects.get_or_create(
            tool=tool,
            user=assigned_user,
            defaults={'notes': f'Asignación de prueba {i+1}'}
        )

# Crear proyectos y actividades (más proyectos para pruebas)
projects_data = []
for i in range(1, 21):  # 20 proyectos
    projects_data.append({
        'name': f'Proyecto {i}',
        'description': f'Descripción del proyecto {i}'
    })

for data in projects_data:
    project, created = Project.objects.get_or_create(
        name=data['name'],
        defaults={'description': data['description']}
    )
    if created:
        # Crear actividades para el proyecto (3-5 actividades por proyecto)
        num_activities = random.randint(3, 5)
        for j in range(num_activities):
            Activity.objects.get_or_create(
                project=project,
                name=f'Actividad {j+1} del Proyecto {project.name}',
                defaults={
                    'progress_percent': random.randint(0, 100),
                    'status': random.choice(['pendiente', 'en_progreso', 'completada'])
                }
            )

print("Datos de prueba para rendimiento agregados exitosamente.")
print(f"- {Material.objects.count()} materiales creados")
print(f"- {Tool.objects.count()} herramientas creadas")
print(f"- {MaterialMovement.objects.count()} movimientos creados")
print(f"- {Project.objects.count()} proyectos creados")
print(f"- {Activity.objects.count()} actividades creadas")
