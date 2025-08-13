from django import forms
from .models import Acudiente
from .models import Jugador

class AcudienteForm(forms.ModelForm):
    class Meta:
        model = Acudiente
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''