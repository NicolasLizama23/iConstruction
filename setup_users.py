from django.contrib.auth.models import User, Group

# Crear grupos
for nombre in ["Administrador", "Bodeguero", "Planificador", "Supervisor", "Analista", "Operario"]:
    Group.objects.get_or_create(name=nombre)
    print(f"Grupo '{nombre}' creado/verificado")

# Crear usuarios
usuarios_datos = [
    ("admin", "Administrador"),
    ("bodeguero", "Bodeguero"),
    ("planificador", "Planificador"),
    ("supervisor", "Supervisor"),
    ("analista", "Analista"),
    ("operario", "Operario"),
]

print("\n=== Creando usuarios ===")
for user_name, role in usuarios_datos:
    u, c = User.objects.get_or_create(username=user_name)
    u.set_password("hola1234")
    u.email = f"{user_name}@iconstruction.local"
    u.save()
    g = Group.objects.get(name=role)
    u.groups.clear()
    u.groups.add(g)
    status = "CREADO" if c else "ACTUALIZADO"
    print(f"  {user_name:15} -> {role:20} [{status}]")

print("\n✓ Usuarios y grupos configurados exitosamente")
print("\nCredenciales:")
for user_name, _ in usuarios_datos:
    print(f"  {user_name} / hola1234")
