import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CEFUSA.settings')
django.setup()

from django.contrib.auth.models import User

print("\n=== RESETEAR CONTRASEÑA DE USUARIO ===\n")

# Listar usuarios
users = User.objects.all()
print("Usuarios disponibles:")
for i, user in enumerate(users, 1):
    print(f"{i}. {user.username} - Staff: {user.is_staff}, Superuser: {user.is_superuser}")

print("\n" + "="*50)
username = input("\nIngresa el username del usuario a modificar: ")

try:
    user = User.objects.get(username=username)
    print(f"\nUsuario encontrado: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Staff: {user.is_staff}")
    print(f"  Superuser: {user.is_superuser}")
    
    nueva_password = input("\nIngresa la NUEVA contraseña: ")
    confirmar_password = input("Confirma la NUEVA contraseña: ")
    
    if nueva_password != confirmar_password:
        print("\n❌ Las contraseñas no coinciden. Intenta de nuevo.")
    elif len(nueva_password) < 4:
        print("\n❌ La contraseña debe tener al menos 4 caracteres.")
    else:
        user.set_password(nueva_password)
        user.save()
        print(f"\n✅ Contraseña actualizada exitosamente para '{username}'")
        print(f"   Ahora puedes iniciar sesión en: http://127.0.0.1:8000/login/")
        print(f"   Username: {username}")
        print(f"   Password: {nueva_password}")

except User.DoesNotExist:
    print(f"\n❌ Usuario '{username}' no encontrado.")
    print("\nUsuarios disponibles:")
    for user in users:
        print(f"  - {user.username}")
