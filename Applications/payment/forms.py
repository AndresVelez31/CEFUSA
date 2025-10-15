from django import forms
from .models import Payment

def create_payment_form():
    class CreatePaymentForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            # Aplicar mensaje de validación en español a todos los campos
            for field_name, field in self.fields.items():
                # Mensaje de validación en español
                field.widget.attrs['oninvalid'] = "this.setCustomValidity('Por favor, completa este campo')"
                field.widget.attrs['oninput'] = "this.setCustomValidity('')"
                
                # Aplicar clases de Bootstrap
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs['class'] = 'form-select'
                elif isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs['class'] = 'form-check-input'
                else:
                    field.widget.attrs['class'] = 'form-control'
        
        class Meta:
            model = Payment
            fields = ['amount', 'description', 'date']
    return CreatePaymentForm

class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Etiquetas en español
        labels = {
            'account': 'Cuenta',
            'date': 'Fecha',
            'description': 'Descripción',
            'branch': 'Sucursal',
            'reference_1': 'Referencia 1',
            'reference_2': 'Referencia 2',
            'amount': 'Valor',
            'player_name': 'Nombre del Jugador',
            'reason': 'Motivo',
            'sales_invoice': 'Factura de Venta',
            'receipt': 'Recibo de Caja',
            'comment': 'Comentario',
            'fk_responsible': 'Responsable',
        }
        
        # Aplicar etiquetas y configuración a todos los campos
        for field_name, field in self.fields.items():
            # Etiquetas en español
            if field_name in labels:
                field.label = labels[field_name]
                
            # Mensaje de validación en español
            field.widget.attrs['oninvalid'] = "this.setCustomValidity('Por favor, completa este campo')"
            field.widget.attrs['oninput'] = "this.setCustomValidity('')"
            
            # Aplicar clases de Bootstrap
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Payment
        fields = '__all__'
