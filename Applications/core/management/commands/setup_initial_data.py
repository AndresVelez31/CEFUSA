"""
Comando para configurar datos iniciales del sistema CEFUSA
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction


class Command(BaseCommand):
    help = 'Configura datos iniciales del sistema CEFUSA (grupos, superusuario por defecto)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Crear un superusuario por defecto si no existe',
        )
        parser.add_argument(
            '--superuser-username',
            type=str,
            default='admin',
            help='Nombre de usuario para el superusuario (por defecto: admin)',
        )
        parser.add_argument(
            '--superuser-email',
            type=str,
            default='admin@cefusa.com',
            help='Email para el superusuario (por defecto: admin@cefusa.com)',
        )
        parser.add_argument(
            '--superuser-password',
            type=str,
            default='admin123',
            help='Contraseña para el superusuario (por defecto: admin123)',
        )

    def handle(self, *args, **options):
        """
        Ejecuta la configuración inicial de datos
        """
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando configuración de datos iniciales de CEFUSA...')
        )

        try:
            with transaction.atomic():
                self._create_groups()
                
                if options['create_superuser']:
                    self._create_superuser(
                        username=options['superuser_username'],
                        email=options['superuser_email'],
                        password=options['superuser_password']
                    )

            self.stdout.write(
                self.style.SUCCESS('✅ Configuración inicial completada exitosamente!')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error durante la configuración: {str(e)}')
            )
            raise

    def _create_groups(self):
        """Crea los grupos predeterminados"""
        self.stdout.write('📋 Verificando grupos predeterminados...')
        
        # Crear grupo Admin
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(
                self.style.SUCCESS('  ✓ Grupo "Admin" creado')
            )
        else:
            self.stdout.write('  → Grupo "Admin" ya existe')

        # Crear grupo Profesor
        profesor_group, created = Group.objects.get_or_create(name='Profesor')
        if created:
            self.stdout.write(
                self.style.SUCCESS('  ✓ Grupo "Profesor" creado')
            )
        else:
            self.stdout.write('  → Grupo "Profesor" ya existe')

    def _create_superuser(self, username, email, password):
        """Crea un superusuario por defecto"""
        self.stdout.write('👤 Verificando superusuario por defecto...')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(f'  → Superusuario "{username}" ya existe')
            return

        # Crear superusuario
        superuser = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Administrador',
            last_name='CEFUSA'
        )

        # Agregar al grupo Admin
        admin_group = Group.objects.get(name='Admin')
        superuser.groups.add(admin_group)

        self.stdout.write(
            self.style.SUCCESS(f'  ✓ Superusuario "{username}" creado y asignado al grupo Admin')
        )
        self.stdout.write(
            self.style.WARNING(f'  ⚠️  Credenciales: {username} / {password}')
        )
        self.stdout.write(
            self.style.WARNING('  🔒 ¡Recuerda cambiar la contraseña por defecto!')
        )