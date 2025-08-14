from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def paymentsManagement(request):
    from django.db.models import Q
    from .models import Pago

    search = request.GET.get('search', '')
    # Filtros avanzados
    cuenta = request.GET.get('cuenta', '')
    fecha = request.GET.get('fecha', '')
    sucursal = request.GET.get('sucursal', '')
    referencia1 = request.GET.get('referencia1', '')
    referencia2 = request.GET.get('referencia2', '')
    nombre = request.GET.get('nombre', '')
    motivo = request.GET.get('motivo', '')
    responsable = request.GET.get('responsable', '')

    pagos = Pago.objects.all()

    # Búsqueda simple
    if search:
        pagos = pagos.filter(
            Q(nombre__icontains=search) |
            Q(motivo__icontains=search) |
            Q(descripcion__icontains=search) |
            Q(referencia1__icontains=search) |
            Q(referencia2__icontains=search) |
            Q(sucursal__icontains=search) |
            Q(factura_venta__icontains=search) |
            Q(recibo_caja__icontains=search) |
            Q(comentario__icontains=search) |
            Q(responsable__nombre__icontains=search) |
            Q(responsable__apellidos__icontains=search)
        )

    # Filtros avanzados
    if cuenta:
        pagos = pagos.filter(cuenta=cuenta)
    if fecha:
        pagos = pagos.filter(fecha=fecha)
    if sucursal:
        pagos = pagos.filter(sucursal__icontains=sucursal)
    if referencia1:
        pagos = pagos.filter(referencia1__icontains=referencia1)
    if referencia2:
        pagos = pagos.filter(referencia2__icontains=referencia2)
    if nombre:
        pagos = pagos.filter(nombre__icontains=nombre)
    if motivo:
        pagos = pagos.filter(motivo__icontains=motivo)
    if responsable:
        pagos = pagos.filter(responsable__id=responsable)

    context = {
        'pagos': pagos,
        'cuentas': Pago.CuentaChoices.choices,
    }
    return render(request, 'paymentsManagement.html', context)

from django.shortcuts import redirect, render
from .models import Pago
from datetime import datetime

def crear_pago(request):
    if request.method == "POST":
        Pago.objects.create(
            cuenta=request.POST.get("cuenta"),
            fecha=request.POST.get("fecha"),
            nombre=request.POST.get("nombre"),
            motivo=request.POST.get("motivo"),
            valor=request.POST.get("valor"),
            referencia1=request.POST.get("referencia1"),
            referencia2=request.POST.get("referencia2"),
            responsable_id=request.POST.get("responsable") or None
        )
        return redirect('gestionar_pagos')  # Redirige a la lista de pagos
