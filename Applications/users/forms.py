from django import forms
from .models import Acudiente
from .models import Jugador

class AcudienteForm(forms.ModelForm):
    class Meta:
        model = Acudiente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ in ['Select', 'SelectMultiple']:
                field.widget.attrs['class'] = 'form-select'
            elif field.widget.__class__.__name__ in ['CheckboxInput', 'RadioSelect']:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ in ['Select', 'SelectMultiple']:
                field.widget.attrs['class'] = 'form-select'
            elif field.widget.__class__.__name__ in ['CheckboxInput', 'RadioSelect']:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'