import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CEFUSA.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

print("\n=== PRUEBA DE LOGIN ===\n")

# Obtener usuarios staff
staff_users = User.objects.filter(is_staff=True)

print("Usuarios con permisos de staff encontrados:")
for user in staff_users:
    print(f"  - {user.username} (Staff: {user.is_staff}, Superuser: {user.is_superuser}, Active: {user.is_active})")

print("\n" + "="*50)
print("PRUEBA DE AUTENTICACIÓN")
print("="*50)

# Intentar autenticar
username = input("\nIngresa tu username: ")
password = input("Ingresa tu password: ")

user = authenticate(username=username, password=password)

if user is not None:
    print(f"\n✅ Autenticación EXITOSA para '{username}'")
    print(f"   - is_active: {user.is_active}")
    print(f"   - is_staff: {user.is_staff}")
    print(f"   - is_superuser: {user.is_superuser}")
    
    if user.is_staff or user.is_superuser:
        print(f"\n✅ El usuario TIENE permisos de administrador")
        print(f"   - Puede acceder al sistema")
    else:
        print(f"\n⚠️  El usuario NO tiene permisos de administrador")
        print(f"   - No puede acceder al sistema")
else:
    print(f"\n❌ Autenticación FALLIDA")
    print(f"   - Usuario o contraseña incorrectos")
    print(f"\n   Verifica que:")
    print(f"   1. El username sea correcto (case-sensitive)")
    print(f"   2. La contraseña sea correcta")
    
    # Verificar si el usuario existe
    try:
        user_check = User.objects.get(username=username)
        print(f"\n   ℹ️  El usuario '{username}' existe en la base de datos")
        print(f"      pero la contraseña es incorrecta")
    except User.DoesNotExist:
        print(f"\n   ℹ️  El usuario '{username}' NO existe en la base de datos")
