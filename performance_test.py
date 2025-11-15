#!/usr/bin/env python3
"""
Script de Pruebas de Rendimiento para iConstruction
Evalúa tiempos de respuesta y estabilidad con grandes volúmenes de datos.

Casos de prueba:
- PT-R-001: Listado de 200+ ítems < 2s
- PT-R-002: Exportación CSV con 5.000 filas ≤ 5s
"""

import os
import django
import time
import csv
import io
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iconstruction_project.settings')
django.setup()

from inventory.models import Material, MaterialMovement
from activities.models import Project, Activity

def measure_time(func):
    """Decorador para medir tiempo de ejecución"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(".2f")
        return result, execution_time
    return wrapper

@measure_time
def test_material_list():
    """PT-R-001: Listado de materiales (200+ ítems)"""
    materials = Material.objects.all().order_by('name')
    count = materials.count()
    # Simular procesamiento de template
    material_list = []
    for material in materials:
        material_list.append({
            'name': material.name,
            'stock': material.stock,
            'unit': material.unit,
            'min_stock': material.min_stock
        })
    return f"Listado de {count} materiales procesado", count

@measure_time
def test_project_list():
    """PT-R-001: Listado de proyectos con actividades"""
    projects = Project.objects.prefetch_related('activities').all()
    count = projects.count()
    project_data = []
    for project in projects:
        activities = project.activities.all()
        project_data.append({
            'name': project.name,
            'description': project.description,
            'activities_count': activities.count(),
            'activities': list(activities.values('name', 'progress_percent', 'status'))
        })
    return f"Listado de {count} proyectos procesado", count

@measure_time
def test_csv_export_materials():
    """PT-R-002: Exportación CSV de materiales (simulado con 5.000 filas)"""
    # Crear datos simulados para 5.000 filas
    materials_data = []
    for i in range(5000):
        materials_data.append({
            'name': f'Material {i+1}',
            'unit': 'kg',
            'stock': 100 + i,
            'min_stock': 10 + (i % 50),
            'description': f'Descripción del material {i+1}'
        })

    # Simular exportación CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Nombre', 'Unidad', 'Stock', 'Stock Mínimo', 'Descripción'])

    for material in materials_data:
        writer.writerow([
            material['name'],
            material['unit'],
            material['stock'],
            material['min_stock'],
            material['description']
        ])

    csv_content = output.getvalue()
    output.close()
    return f"CSV con {len(materials_data)} filas generado", len(materials_data)

@measure_time
def test_csv_export_movements():
    """PT-R-002: Exportación CSV de movimientos de inventario"""
    movements = MaterialMovement.objects.select_related('material', 'user').all()
    count = movements.count()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Fecha', 'Tipo', 'Material', 'Cantidad', 'Usuario', 'Notas'])

    for movement in movements:
        writer.writerow([
            movement.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            movement.get_kind_display(),
            movement.material.name,
            movement.quantity,
            movement.user.username if movement.user else '',
            movement.notes
        ])

    csv_content = output.getvalue()
    output.close()
    return f"CSV de movimientos con {count} filas generado", count

@measure_time
def test_dashboard_stats():
    """Prueba de carga del dashboard con estadísticas"""
    stats = {
        'materials': Material.objects.count(),
        'tools': 50,  # Simulado
        'projects': Project.objects.count(),
        'activities': Activity.objects.count(),
        'low_stock': Material.objects.filter(stock__lte=100).count(),
    }

    recent_movs = MaterialMovement.objects.select_related('material','user').order_by('-created_at')[:10]
    recent_movements = []
    for mov in recent_movs:
        recent_movements.append({
            'created_at': mov.created_at,
            'kind': mov.kind,
            'material': mov.material.name,
            'quantity': mov.quantity,
            'user': mov.user.username if mov.user else ''
        })

    return f"Dashboard con {stats['materials']} materiales, {stats['projects']} proyectos procesado", stats

def run_performance_tests():
    """Ejecutar todas las pruebas de rendimiento"""
    print("=" * 60)
    print("PRUEBAS DE RENDIMIENTO - iCONSTRUCTION")
    print("=" * 60)
    print(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # PT-R-001: Listados
    print("PT-R-001: Listado de 200+ ítems < 2s")
    print("-" * 40)

    result, time_taken = test_material_list()
    print(f"Resultado: {result}")
    status = "✅ PASÓ" if time_taken < 2.0 else "❌ FALLÓ"
    print(f"Estado: {status} (Objetivo: < 2.0s)")
    print()

    result, time_taken = test_project_list()
    print(f"Resultado: {result}")
    status = "✅ PASÓ" if time_taken < 2.0 else "❌ FALLÓ"
    print(f"Estado: {status} (Objetivo: < 2.0s)")
    print()

    # PT-R-002: Exportaciones CSV
    print("PT-R-002: Exportación CSV con 5.000 filas ≤ 5s")
    print("-" * 40)

    result, time_taken = test_csv_export_materials()
    print(f"Resultado: {result}")
    status = "✅ PASÓ" if time_taken <= 5.0 else "❌ FALLÓ"
    print(f"Estado: {status} (Objetivo: ≤ 5.0s)")
    print()

    result, time_taken = test_csv_export_movements()
    print(f"Resultado: {result}")
    status = "✅ PASÓ" if time_taken <= 5.0 else "❌ FALLÓ"
    print(f"Estado: {status} (Objetivo: ≤ 5.0s)")
    print()

    # Prueba adicional del dashboard
    print("PRUEBA ADICIONAL: Dashboard Stats")
    print("-" * 40)

    result, time_taken = test_dashboard_stats()
    print(f"Resultado: {result}")
    status = "✅ PASÓ" if time_taken < 1.0 else "❌ FALLÓ"
    print(f"Estado: {status} (Objetivo: < 1.0s)")
    print()

    print("=" * 60)
    print("RECOMENDACIONES PARA OPTIMIZACIÓN:")
    print("- Implementar paginación para listados grandes")
    print("- Usar select_related/prefetch_related en consultas")
    print("- Considerar índices en campos de búsqueda frecuente")
    print("- Implementar cache para estadísticas del dashboard")
    print("- Optimizar consultas N+1 en listados de proyectos/actividades")
    print("=" * 60)

if __name__ == "__main__":
    run_performance_tests()
