import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iconstruction_project.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from inventory.models import Material, Tool, MaterialMovement, ToolAssignment
from activities.models import Project, Activity

# Obtener content types
ct_material = ContentType.objects.get_for_model(Material)
ct_tool = ContentType.objects.get_for_model(Tool)
ct_movement = ContentType.objects.get_for_model(MaterialMovement)
ct_toolassign = ContentType.objects.get_for_model(ToolAssignment)
ct_project = ContentType.objects.get_for_model(Project)
ct_activity = ContentType.objects.get_for_model(Activity)

# Crear grupos y asignar permisos
roles = {
    'Administrador': [
        ('material', 'add_material'),
        ('material', 'change_material'),
        ('material', 'delete_material'),
        ('material', 'view_material'),
        ('tool', 'add_tool'),
        ('tool', 'change_tool'),
        ('tool', 'delete_tool'),
        ('tool', 'view_tool'),
        ('materialmove', 'add_materialmove'),
        ('materialmove', 'change_materialmove'),
        ('materialmove', 'delete_materialmove'),
        ('materialmove', 'view_materialmove'),
        ('toolassign', 'add_toolassignment'),
        ('toolassign', 'change_toolassignment'),
        ('toolassign', 'delete_toolassignment'),
        ('toolassign', 'view_toolassignment'),
        ('project', 'add_project'),
        ('project', 'change_project'),
        ('project', 'delete_project'),
        ('project', 'view_project'),
        ('activity', 'add_activity'),
        ('activity', 'change_activity'),
        ('activity', 'delete_activity'),
        ('activity', 'view_activity'),
    ],
    'Bodeguero': [
        ('material', 'add_material'),
        ('material', 'change_material'),
        ('material', 'view_material'),
        ('materialmove', 'add_materialmove'),
        ('materialmove', 'change_materialmove'),
        ('materialmove', 'view_materialmove'),
    ],
    'Planificador': [
        ('material', 'view_material'),
        ('project', 'add_project'),
        ('project', 'change_project'),
        ('project', 'view_project'),
        ('activity', 'add_activity'),
        ('activity', 'change_activity'),
        ('activity', 'view_activity'),
    ],
    'Supervisor': [
        ('material', 'view_material'),
        ('materialmove', 'view_materialmove'),
        ('project', 'view_project'),
        ('activity', 'view_activity'),
        ('tool', 'view_tool'),
        ('toolassign', 'view_toolassignment'),
    ],
    'Analista': [
        ('material', 'view_material'),
        ('materialmove', 'view_materialmove'),
        ('project', 'view_project'),
        ('activity', 'view_activity'),
        ('tool', 'view_tool'),
    ],
    'Operario': [
        ('material', 'view_material'),
        ('project', 'view_project'),
        ('activity', 'view_activity'),
    ],
}

ct_map = {
    'material': ct_material,
    'tool': ct_tool,
    'materialmove': ct_movement,
    'toolassign': ct_toolassign,
    'project': ct_project,
    'activity': ct_activity,
}

for role_name, perms in roles.items():
    group, created = Group.objects.get_or_create(name=role_name)
    group.permissions.clear()
    for model_name, codename in perms:
        ct = ct_map.get(model_name)
        if ct:
            try:
                perm = Permission.objects.get(content_type=ct, codename=codename)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                print(f'  [WARN] Permiso {codename} no encontrado para {model_name}')
    print(f'{role_name}: {group.permissions.count()} permisos asignados')

# Crear usuarios por rol
usuarios_roles = {
    'admin': 'Administrador',
    'bodeguero': 'Bodeguero',
    'planificador': 'Planificador',
    'supervisor': 'Supervisor',
    'analista': 'Analista',
    'operario': 'Operario',
}

print('\n=== USUARIOS ===')
for username, role in usuarios_roles.items():
    user, created = User.objects.get_or_create(username=username)
    user.set_password('hola1234')
    user.email = f'{username}@iconstruction.local'
    user.save()
    group = Group.objects.get(name=role)
    user.groups.clear()
    user.groups.add(group)
    status = 'CREADO' if created else 'ACTUALIZADO'
    print(f'  {username} ({role}): {status}')

print('\n✓ Grupos y usuarios configurados exitosamente')
