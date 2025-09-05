from django import forms
from .models import Pago

def crear_pago_form():
    class CrearPagoForm(forms.ModelForm):
        class Meta:
            model = Pago
            fields = ['monto', 'descripcion', 'fecha']
    return CrearPagoForm

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'
