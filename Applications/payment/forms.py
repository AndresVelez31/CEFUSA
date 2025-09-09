from django import forms
from .models import Payment

def create_payment_form():
    class CreatePaymentForm(forms.ModelForm):
        class Meta:
            model = Payment
            fields = ['amount', 'description', 'date']
    return CreatePaymentForm

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
