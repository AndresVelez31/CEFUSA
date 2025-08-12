from django import forms
from .models import Acudiente
from .models import Jugador

class AcudienteForm(forms.ModelForm):
    class Meta:
        model = Acudiente
        fields = '__all__'

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = '__all__'