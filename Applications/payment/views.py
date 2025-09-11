from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import Payment
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from django.db.models import Q

from .models import Payment
from Applications.user.models import Guardian
from .forms import PaymentForm

# Create your views here.
def display_payment(request):
    search = request.GET.get('search', '')
    # Filtros avanzados
    account = request.GET.get('account', '')
    date = request.GET.get('date', '')
    branch = request.GET.get('branch', '')
    reference_1 = request.GET.get('reference_1', '')
    reference_2 = request.GET.get('reference_2', '')
    player_name = request.GET.get('player_name', '')
    reason = request.GET.get('reason', '')
    fk_responsible = request.GET.get('fk_responsible', '')
    sales_invoice = request.GET.get('sales_invoice', '')

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
    if fk_responsible:
        payments = payments.filter(fk_responsible__id=fk_responsible)
    if sales_invoice:
        payments = payments.filter(sales_invoice__icontains=sales_invoice)

    # Para el template: payments, accounts, responsibles, total_results

    responsibles = Guardian.objects.all()
    context = {
        'payments': payments,
        'accounts': Payment.AccountChoices.choices,
        'responsibles': responsibles,
        'total_results': payments.count(),
    }
    return render(request, 'payment_management.html', context)

def create_payment(request):
    if request.method == "POST":
        Payment.objects.create(
            account=request.POST.get("account"),
            date=request.POST.get("date"),
            description=request.POST.get("description"),
            branch=request.POST.get("branch"),
            reference_1=request.POST.get("reference_1"),
            reference_2=request.POST.get("reference_2"),
            amount=request.POST.get("amount"),
            player_name=request.POST.get("player_name"),
            reason=request.POST.get("reason"),
            sales_invoice=request.POST.get("sales_invoice"),
            receipt=request.POST.get("receipt"),
            comment=request.POST.get("comment"),
            fk_responsible_id=request.POST.get("responsible") or None
        )
    return redirect('payment_management')  # Redirect to payments list

## cambiar a get_edit_form
def get_payment_edit_form(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    form = PaymentForm(instance=payment)
    # Debug: print form fields and errors
    print('DEBUG PaymentForm fields:', form.fields.keys())
    print('DEBUG PaymentForm errors:', form.errors)
    print('DEBUG Payment object:', payment)
    html = render_to_string('get_payment_edit_form.html', {'form': form, 'payment': payment}, request=request)
    if not html.strip():
        print('DEBUG: Rendered HTML for edit form is empty!')
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
                return redirect(reverse('display_payment'))
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
    return redirect(reverse('display_payment'))

def get_payment_details(request, payment_id):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Petición inválida.'}, status=400)
    
    payment = get_object_or_404(Payment, id=payment_id)
    payment_data = {
        'id': payment.id,
        'account': payment.account,  # <-- código, no display
        'date': payment.date.strftime('%Y-%m-%d') if payment.date else '',  # <-- formato ISO
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
