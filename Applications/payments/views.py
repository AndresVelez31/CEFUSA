from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import Pago
from .forms import PagoForm

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

def edit_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    form = PagoForm(instance=pago)
    html = render_to_string('payments/partials/editar_pago_form.html', {'form': form, 'pago': pago}, request=request)
    return HttpResponse(html)

def update_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                from django.urls import reverse
                from django.shortcuts import redirect
                return redirect(reverse('paymentsManagement'))
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('payments/partials/editar_pago_form.html', {'form': form, 'pago': pago}, request=request)
                return JsonResponse({'success': False, 'html': html})
            else:
                return render(request, 'payments/partials/editar_pago_form.html', {'form': form, 'pago': pago})
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
    else:
        from django.urls import reverse
        from django.shortcuts import redirect
    return redirect(reverse('paymentsManagement'))
