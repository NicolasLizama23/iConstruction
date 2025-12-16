from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Crea usuarios demo y grupos si no existen (idempotente)."

    def handle(self, *args, **options):
        User = get_user_model()

        demo_password = "hola1234"

        # (Opcional) crea grupos
        group_names = ["Bodeguero", "Planificador", "Supervisor", "Analista", "Operario", "Administrador"]
        groups = {}
        for name in group_names:
            g, _ = Group.objects.get_or_create(name=name)
            groups[name] = g

        # username -> grupo
        users = [
            ("admin", "Administrador", True),
            ("bodeguero", "Bodeguero", False),
            ("planificador", "Planificador", False),
            ("supervisor", "Supervisor", False),
            ("analista", "Analista", False),
            ("operario", "Operario", False),
        ]

        for username, group_name, is_staff_admin in users:
            user, created = User.objects.get_or_create(username=username, defaults={
                "is_staff": is_staff_admin,
                "is_superuser": is_staff_admin,
                "is_active": True,
            })

            # Asegura flags (si ya existía)
            if is_staff_admin:
                user.is_staff = True
                user.is_superuser = True

            # Setea password SIEMPRE de forma correcta (hash)
            user.set_password(demo_password)
            user.save()

            # Asigna grupo
            if group_name in groups:
                user.groups.add(groups[group_name])

            self.stdout.write(self.style.SUCCESS(
                f"{'CREATED' if created else 'UPDATED'} user {username} / pass={demo_password}"
            ))
