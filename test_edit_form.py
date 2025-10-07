#!/usr/bin/env python3
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CEFUSA.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from Applications.payment.models import Payment

print("=== PROBANDO LA URL DE GET_PAYMENT_EDIT_FORM ===")
print()

# Crear un cliente de prueba
client = Client()

# Obtener un usuario Admin
admin_user = User.objects.filter(groups__name='Admin').first()
if not admin_user:
    print("❌ No se encontró ningún usuario Admin")
    exit()

print(f"✅ Usuario Admin encontrado: {admin_user.username}")

# Hacer login
client.force_login(admin_user)
print("✅ Login realizado")

# Obtener un pago de ejemplo
payment = Payment.objects.first()
if not payment:
    print("❌ No hay pagos en la base de datos para probar")
    exit()

print(f"✅ Pago encontrado: ID {payment.id}")

# Probar la URL
url = f'/payment/pagos/{payment.id}/edit/'
print(f"🔍 Probando URL: {url}")

response = client.get(url)
print(f"📊 Status Code: {response.status_code}")
print(f"📊 Content-Type: {response.get('Content-Type', 'No definido')}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    if content.startswith('<'):
        print("✅ Respuesta es HTML (correcto)")
        print(f"📝 Primeras 100 caracteres: {content[:100]}...")
    else:
        print("❌ Respuesta no parece ser HTML")
        print(f"📝 Contenido: {content}")
elif response.status_code == 403:
    print("❌ Error 403: Sin permisos")
    print(f"📝 Contenido: {response.content.decode('utf-8')}")
else:
    print(f"❌ Error {response.status_code}")
    print(f"📝 Contenido: {response.content.decode('utf-8')}")