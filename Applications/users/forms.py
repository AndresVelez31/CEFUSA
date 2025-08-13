# users/forms.py
from django import forms
from .models import Acudiente, Jugador

class AcudienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.editable = kwargs.pop('editable', False)
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.help_text = ''
            
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
            if field_name in ['tipo_doc', 'tipo_regimen']:
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            
            if not self.editable and not self.instance._state.adding:
                if isinstance(field.widget, (forms.Select, forms.CheckboxInput)):
                    field.widget.attrs['disabled'] = True
                else:
                    field.widget.attrs['readonly'] = True

    class Meta:
        model = Acudiente
        fields = '__all__'

class JugadorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.editable = kwargs.pop('editable', False)
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.help_text = ''
            
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
            if field_name in ['tipo_doc', 'jornada_entreno', 'acudiente']:
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            
            # Configuración especial para el campo de fecha
            if field_name == 'fecha_nacimiento':
                field.widget.attrs['type'] = 'date'
                field.widget.attrs['class'] = 'form-control datepicker'
                # Establecer el formato de fecha si es necesario
                field.widget.format = '%Y-%m-%d'
                field.input_formats = ['%Y-%m-%d']
            
            if not self.editable and not self.instance._state.adding:
                if isinstance(field.widget, (forms.Select, forms.CheckboxInput)):
                    field.widget.attrs['disabled'] = True
                else:
                    field.widget.attrs['readonly'] = True

    class Meta:
        model = Jugador
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control datepicker'
                },
                format='%Y-%m-%d'
            )
        }