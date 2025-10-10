"""
Comando para asignar roles a usuarios existentes
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.db import transaction


class Command(BaseCommand):
    help = 'Asigna roles (Admin/Profesor) a usuarios existentes'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='Nombre de usuario al que asignar el rol'
        )
        parser.add_argument(
            'role',
            type=str,
            choices=['Admin', 'Profesor'],
            help='Rol a asignar: Admin o Profesor'
        )
        parser.add_argument(
            '--remove',
            action='store_true',
            help='Remover el rol en lugar de asignarlo'
        )

    def handle(self, *args, **options):
        username = options['username']
        role = options['role']
        remove = options['remove']

        try:
            # Verificar que el usuario existe
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'Usuario "{username}" no existe')

        try:
            # Verificar que el grupo existe
            group = Group.objects.get(name=role)
        except Group.DoesNotExist:
            raise CommandError(f'El grupo "{role}" no existe. Ejecuta primero: python manage.py migrate')

        if remove:
            # Remover del grupo
            if user.groups.filter(name=role).exists():
                user.groups.remove(group)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Rol "{role}" removido del usuario "{username}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ El usuario "{username}" no tenía el rol "{role}"')
                )
        else:
            # Asignar al grupo
            if user.groups.filter(name=role).exists():
                self.stdout.write(
                    self.style.WARNING(f'→ El usuario "{username}" ya tiene el rol "{role}"')
                )
            else:
                user.groups.add(group)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Rol "{role}" asignado al usuario "{username}"')
                )

        # Mostrar roles actuales del usuario
        user_groups = user.groups.all()
        if user_groups:
            roles = [group.name for group in user_groups]
            self.stdout.write(f'📋 Roles actuales de "{username}": {", ".join(roles)}')
        else:
            self.stdout.write(f'📋 El usuario "{username}" no tiene roles asignados')