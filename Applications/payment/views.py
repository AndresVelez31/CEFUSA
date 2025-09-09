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
    from django.db.models import Q
    from .models import Pago

    search = request.GET.get('search', '')
    # Filtros avanzados
    account = request.GET.get('account', '')
    date = request.GET.get('date', '')
    branch = request.GET.get('branch', '')
    reference_1 = request.GET.get('reference_1', '')
    reference_2 = request.GET.get('reference_2', '')
    player_name = request.GET.get('player_name', '')
    reason = request.GET.get('reason', '')
    responsible = request.GET.get('responsible', '')

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
            Q(fk_responsible__nombre__icontains=search) |
            Q(fk_responsible__apellidos__icontains=search)
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

    total_results = payments.count()

    responsables = Acudiente.objects.all()

    context = {
        'payments': payments,
        'accounts': Payment.AccountChoices.choices,
    }
    return render(request, 'payment_management.html', context)

def create_payment(request):
    if request.method == "POST":
        Payment.objects.create(
            account=request.POST.get("account"),
            date=request.POST.get("date"),
            player_name=request.POST.get("player_name"),
            reason=request.POST.get("reason"),
            value=request.POST.get("value"),
            reference_1=request.POST.get("reference_1"),
            reference_2=request.POST.get("reference_2"),
            responsible_id=request.POST.get("responsible") or None
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
