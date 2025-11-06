import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CEFUSA.settings')
django.setup()

from django.contrib.auth.models import User

print("\n=== USUARIOS EN LA BASE DE DATOS ===\n")
users = User.objects.all()

if users.count() == 0:
    print("⚠️  No hay usuarios en la base de datos.")
else:
    for user in users:
        print(f"Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Staff: {user.is_staff}")
        print(f"  Superuser: {user.is_superuser}")
        print(f"  Active: {user.is_active}")
        print("-" * 50)

print(f"\nTotal usuarios: {users.count()}")

# Ofrecer crear un superusuario si no hay ninguno
if not User.objects.filter(is_superuser=True).exists():
    print("\n⚠️  No hay ningún superusuario en la base de datos.")
    print("\n¿Deseas crear un superusuario ahora?")
    respuesta = input("Escribe 'si' para crear uno: ").lower()
    
    if respuesta == 'si':
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        
        user = User.objects.create_superuser(username=username, email=email, password=password)
        print(f"\n✅ Superusuario '{username}' creado exitosamente!")
        print(f"   Puedes iniciar sesión en: http://127.0.0.1:8000/login/")
