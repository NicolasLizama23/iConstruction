import os
import django
from django.utils import timezone
from datetime import timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iconstruction_project.settings')

# Primero intentar con MySQL, si falla cambiar a SQLite
try:
    django.setup()
    from django.db import connection
    connection.ensure_connection()
except Exception as e:
    print(f"⚠️  Error conectando a MySQL: {str(e)[:100]}")
    print("   Cambiando a SQLite temporalmente...")
    
    # Cambiar settings a SQLite
    from django.conf import settings
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(__file__), 'db_demo.sqlite3'),
        }
    }
    django.setup()

from inventory.models import Material, Tool, MaterialMovement, ToolAssignment
from activities.models import Project, Activity, ActivityLog
from django.contrib.auth.models import User

print("=" * 60)
print("🏗️  CREANDO DATOS DE EJEMPLO PARA ICONSTRUCTION")
print("=" * 60)

# Obtener usuarios para asignar
users = list(User.objects.all()[:5])
if not users:
    print("❌ No hay usuarios en la BD. Ejecuta setup_users.py primero.")
    exit(1)

# ============================================================
# 1. CREAR MATERIALES DE EJEMPLO
# ============================================================
print("\n📦 Creando materiales...")
materiales_data = [
    {'name': 'Cemento Portland', 'unit': 'kg', 'stock': 5000, 'min_stock': 500},
    {'name': 'Arena gruesa', 'unit': 'm3', 'stock': 150, 'min_stock': 20},
    {'name': 'Ripio', 'unit': 'm3', 'stock': 200, 'min_stock': 30},
    {'name': 'Ladrillos', 'unit': 'un', 'stock': 10000, 'min_stock': 1000},
    {'name': 'Tuberías PVC', 'unit': 'un', 'stock': 500, 'min_stock': 50},
    {'name': 'Cables eléctricos', 'unit': 'm', 'stock': 2000, 'min_stock': 200},
    {'name': 'Acero de refuerzo', 'unit': 'kg', 'stock': 3000, 'min_stock': 300},
    {'name': 'Pintura', 'unit': 'lt', 'stock': 800, 'min_stock': 100},
]

materiales_creados = []
for data in materiales_data:
    mat, created = Material.objects.get_or_create(
        name=data['name'],
        defaults={
            'unit': data['unit'],
            'stock': data['stock'],
            'min_stock': data['min_stock']
        }
    )
    materiales_creados.append(mat)
    status = "✓ CREADO" if created else "  (existente)"
    print(f"  {mat.name:25} - Stock: {mat.stock} {mat.unit} {status}")

# ============================================================
# 2. CREAR HERRAMIENTAS DE EJEMPLO
# ============================================================
print("\n🔧 Creando herramientas...")
herramientas_data = [
    {'name': 'Excavadora', 'code': 'EXCA001', 'status': 'disponible'},
    {'name': 'Grúa móvil', 'code': 'GRUA001', 'status': 'disponible'},
    {'name': 'Compresor', 'code': 'COMP001', 'status': 'asignada'},
    {'name': 'Sierra circular', 'code': 'SIER001', 'status': 'disponible'},
    {'name': 'Taladro industrial', 'code': 'TALD001', 'status': 'disponible'},
    {'name': 'Hormigonera', 'code': 'HORM001', 'status': 'asignada'},
    {'name': 'Andamios', 'code': 'ANDA001', 'status': 'asignada'},
    {'name': 'Carretilla elevadora', 'code': 'CARE001', 'status': 'disponible'},
]

herramientas_creadas = []
for data in herramientas_data:
    tool, created = Tool.objects.get_or_create(
        code=data['code'],
        defaults={
            'name': data['name'],
            'status': data['status']
        }
    )
    herramientas_creadas.append(tool)
    status = "✓ CREADO" if created else "  (existente)"
    print(f"  {tool.name:25} ({tool.code}) - {tool.status:15} {status}")

# ============================================================
# 3. ASIGNAR ALGUNAS HERRAMIENTAS A USUARIOS
# ============================================================
print("\n👤 Asignando herramientas a usuarios...")
herramientas_asignadas = herramientas_creados[2:5]
for tool in herramientas_asignadas:
    user = random.choice(users)
    assign, created = ToolAssignment.objects.get_or_create(
        tool=tool,
        user=user,
        defaults={
            'notes': f'Asignación de prueba para {user.username}'
        }
    )
    status = "✓ ASIGNADO" if created else "  (existente)"
    print(f"  {tool.name:20} → {user.username:15} {status}")

# ============================================================
# 4. REGISTRAR MOVIMIENTOS DE MATERIALES
# ============================================================
print("\n📊 Registrando movimientos de materiales...")
movimientos_count = 0
for _ in range(15):
    material = random.choice(materiales_creados)
    user = random.choice(users)
    kind = random.choice(['ingreso', 'salida'])
    quantity = random.randint(10, 500)
    
    mov, created = MaterialMovement.objects.get_or_create(
        material=material,
        user=user,
        kind=kind,
        quantity=quantity,
        defaults={
            'notes': f'Movimiento de {kind} de prueba'
        }
    )
    if created:
        movimientos_count += 1

print(f"  ✓ {movimientos_count} movimientos registrados")

# ============================================================
# 5. CREAR PROYECTOS
# ============================================================
print("\n🏢 Creando proyectos...")
proyectos_data = [
    {
        'name': 'Construcción Centro Comercial Downtown',
        'description': 'Proyecto de construcción de centro comercial de 5 pisos ubicado en zona céntrica. Incluye estacionamientos, locales comerciales y área de oficinas.'
    },
    {
        'name': 'Remodelación Edificio Administrativo',
        'description': 'Remodelación completa del edificio administrativo. Incluye actualización de sistemas eléctricos, plomería y acabados.'
    },
    {
        'name': 'Puente Vehicular San José',
        'description': 'Construcción de nuevo puente vehicular que conectará las comunas de San José y Las Condes. Largo total: 2.5 km.'
    },
    {
        'name': 'Complejo Residencial Parque del Sur',
        'description': 'Desarrollo inmobiliario con 150 departamentos, áreas verdes comunes y servicios complementarios.'
    },
    {
        'name': 'Escuela Municipal Nueva Esperanza',
        'description': 'Construcción de nueva infraestructura educativa con capacidad para 800 estudiantes.'
    },
]

proyectos_creados = []
for data in proyectos_data:
    project, created = Project.objects.get_or_create(
        name=data['name'],
        defaults={
            'description': data['description']
        }
    )
    proyectos_creados.append(project)
    status = "✓ CREADO" if created else "  (existente)"
    print(f"  {project.name:45} {status}")

# ============================================================
# 6. CREAR ACTIVIDADES PARA CADA PROYECTO
# ============================================================
print("\n✅ Creando actividades para cada proyecto...")
actividades_estados = ['pendiente', 'en_progreso', 'completada']

for project in proyectos_creados:
    num_actividades = random.randint(3, 6)
    
    for i in range(num_actividades):
        status = random.choice(actividades_estados)
        if status == 'completada':
            progress = 100
        elif status == 'en_progreso':
            progress = random.randint(20, 90)
        else:
            progress = 0
        
        activity, created = Activity.objects.get_or_create(
            project=project,
            name=f'Fase {i+1}: {random.choice(["Excavación", "Cimentación", "Estructura", "Instalaciones", "Acabados", "Pintura"])}',
            defaults={
                'progress_percent': progress,
                'status': status,
                'description': f'Actividad {i+1} del proyecto {project.name}'
            }
        )
        
        if created:
            # Crear logs de avance
            if status in ['en_progreso', 'completada']:
                for j in range(random.randint(1, 4)):
                    ActivityLog.objects.get_or_create(
                        activity=activity,
                        user=random.choice(users),
                        progress_percent=random.randint(activity.progress_percent - 20, activity.progress_percent),
                        defaults={
                            'notes': f'Actualización de progreso {j+1}'
                        }
                    )
            
            print(f"    ✓ {activity.name:40} ({status:12}) - Avance: {activity.progress_percent}%")

# ============================================================
# RESUMEN FINAL
# ============================================================
print("\n" + "=" * 60)
print("✨ DATOS DE EJEMPLO CREADOS EXITOSAMENTE")
print("=" * 60)
print(f"\n📊 RESUMEN:")
print(f"  • Materiales: {Material.objects.count()}")
print(f"  • Herramientas: {Tool.objects.count()}")
print(f"  • Asignaciones de herramientas: {ToolAssignment.objects.count()}")
print(f"  • Movimientos de materiales: {MaterialMovement.objects.count()}")
print(f"  • Proyectos: {Project.objects.count()}")
print(f"  • Actividades: {Activity.objects.count()}")
print(f"  • Registros de avance: {ActivityLog.objects.count()}")

print(f"\n🌐 Accede a: http://127.0.0.1:8000/dashboard/")
print(f"👤 Usuarios disponibles:")
print(f"   - admin / hola1234")
print(f"   - bodeguero / hola1234")
print(f"   - planificador / hola1234")
print(f"   - supervisor / hola1234")
print(f"\n✅ ¡Sistema listo para demostración!")
print("=" * 60)
