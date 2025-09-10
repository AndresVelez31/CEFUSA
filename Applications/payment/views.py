from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import Payment
from .forms import PaymentForm
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.shortcuts import redirect, render
from datetime import datetime
from ..user.models import Guardian
# Create your views here.

def display_payment(request):

    # Obtener y limpiar parámetros de búsqueda (eliminar espacios extra)
    search = request.GET.get('search', '').strip()
    # Filtros avanzados
    account = request.GET.get('account', '').strip()
    date = request.GET.get('date', '').strip()
    branch = request.GET.get('branch', '').strip()
    reference_1 = request.GET.get('reference_1', '').strip()
    reference_2 = request.GET.get('reference_2', '').strip()
    player_name = request.GET.get('player_name', '').strip()
    reason = request.GET.get('reason', '').strip()
    responsible = request.GET.get('fk_responsible', '').strip()
    sales_invoice = request.GET.get('sales_invoice', '').strip()

    payments = Payment.objects.all()

    # Búsqueda simple
    if search:
        payments = payments.filter(
            Q(player_name__icontains=search) |
            Q(reason__icontains=search) |
            Q(description__icontains=search) |
            Q(reference_1__icontains=search) |
            Q(reference_2__icontains=search) |
            Q(branch__icontains=search) |
            Q(sales_invoice__icontains=search) |
            Q(receipt__icontains=search) |
            Q(comment__icontains=search) |
            Q(fk_responsible__first_name__icontains=search) |
            Q(fk_responsible__last_name__icontains=search)
        )

    # Filtros avanzados
    if account:
        payments = payments.filter(account=account)
    if date:
        payments = payments.filter(date=date)
    if branch:
        payments = payments.filter(branch__icontains=branch)
    if reference_1:
        payments = payments.filter(reference_1__icontains=reference_1)
    if reference_2:
        payments = payments.filter(reference_2__icontains=reference_2)
    if player_name:
        payments = payments.filter(player_name__icontains=player_name)
    if reason:
        payments = payments.filter(reason__icontains=reason)
    if responsible:
        payments = payments.filter(fk_responsible__id=responsible)
    if sales_invoice:
        payments = payments.filter(sales_invoice__icontains=sales_invoice)

    total_results = payments.count()

    responsibles = Guardian.objects.all()

    context = {
        'payments': payments,
        'accounts': Payment.AccountChoices.choices,
        'responsibles': responsibles,
        'total_results': total_results,
    }
    return render(request, 'payment_management.html', context)

def create_payment(request):
    if request.method == "POST":
        Payment.objects.create(
            account=request.POST.get("account"),
            date=request.POST.get("date"),
            player_name=request.POST.get("player_name"),
            reason=request.POST.get("reason"),
            amount=request.POST.get("amount"),
            reference_1=request.POST.get("reference_1") or None,
            sales_invoice=request.POST.get("sales_invoice") or None,
            reference_2=request.POST.get("reference_2") or None,
            fk_responsible_id=request.POST.get("responsible") or None,
            description=request.POST.get("description") or None,
            branch=request.POST.get("branch") or None,
            receipt=request.POST.get("receipt") or None,
            comment=request.POST.get("comment") or None
        )
        return redirect('payment_management')  # Redirige a la lista de pagos

## cambiar a get_edit_form
def get_payment_edit_form(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    form = PaymentForm(instance=payment)
    html = render_to_string('get_payment_edit_form.html', {'form': form, 'payment': payment}, request=request)
    return HttpResponse(html)

def update_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                from django.urls import reverse
                from django.shortcuts import redirect
                return redirect(reverse('payment_management'))
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('get_payment_edit_form.html', {'form': form, 'payment': payment}, request=request)
                return JsonResponse({'success': False, 'html': html})
            else:
                return render(request, 'get_payment_edit_form.html', {'form': form, 'payment': payment})
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
    else:
        from django.urls import reverse
        from django.shortcuts import redirect
    return redirect(reverse('payment_management'))

def get_payment_details(request, payment_id):
    """Vista para obtener los detalles de un pago específico"""
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Petición inválida.'}, status=400)
    
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Preparar los datos del pago
    payment_data = {
        'id': payment.id,
        'account': payment.get_account_display(),
        'date': payment.date.strftime('%d/%m/%Y') if payment.date else '',
        'description': payment.description or '',
        'branch': payment.branch or '',
        'reference_1': payment.reference_1 or '',
        'reference_2': payment.reference_2 or '',
        'amount': str(payment.amount),
        'player_name': payment.player_name or '',
        'reason': payment.reason or '',
        'sales_invoice': payment.sales_invoice or '',
        'receipt': payment.receipt or '',
        'comment': payment.comment or '',
        'responsible': {
            'name': f"{payment.fk_responsible.first_name} {payment.fk_responsible.last_name}" if payment.fk_responsible else 'No asignado',
            'id': payment.fk_responsible.id if payment.fk_responsible else None
        }
    }
    
    return JsonResponse(payment_data)

@require_POST
def delete_payment(request, payment_id):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Petición inválida.'}, status=400)
    payment = get_object_or_404(Payment, id=payment_id)
    try:
        payment.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)