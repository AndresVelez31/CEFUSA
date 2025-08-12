# users/forms.py
from django import forms
from .models import Acudiente, Jugador

class AcudienteForm(forms.ModelForm):
    class Meta:
        model = Acudiente
        fields = [
            'tipo_doc', 'identificacion', 'nombre', 'apellidos',
            'ciudad', 'direccion', 'telefono', 'correo', 'tipo_regimen'
        ]
        widgets = {
            # por defecto readonly/disabled: lectura
            'tipo_doc': forms.Select(attrs={'class': 'form-select usuario-field', 'disabled': True}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'nombre': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'tipo_regimen': forms.Select(attrs={'class': 'form-select usuario-field', 'disabled': True}),
        }

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = [
            'tipo_doc', 'identificacion', 'nombre', 'apellido', 'fecha_nacimiento',
            'ciudad_nacimiento', 'direccion', 'ciudad', 'institucion_educativa',
            'jornada_entreno', 'tiene_enfermedad', 'tipo_enfermedad',
            'tiene_contraindicacion', 'contacto_emergencia', 'num_contacto',
            'eps', 'parentesco', 'centro_atencion',
            'pdf_doc_id', 'pdf_certificado_eps', 'acudiente'
        ]
        widgets = {
            'tipo_doc': forms.Select(attrs={'class': 'form-select usuario-field', 'disabled': True}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'nombre': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'apellido': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control usuario-field', 'type': 'date', 'readonly': True}),
            'ciudad_nacimiento': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'institucion_educativa': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'jornada_entreno': forms.Select(attrs={'class': 'form-select usuario-field', 'disabled': True}),
            'tiene_enfermedad': forms.CheckboxInput(attrs={'class': 'form-check-input usuario-field', 'disabled': True}),
            'tipo_enfermedad': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'tiene_contraindicacion': forms.CheckboxInput(attrs={'class': 'form-check-input usuario-field', 'disabled': True}),
            'contacto_emergencia': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'num_contacto': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'eps': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'parentesco': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'centro_atencion': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'pdf_doc_id': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'pdf_certificado_eps': forms.TextInput(attrs={'class': 'form-control usuario-field', 'readonly': True}),
            'acudiente': forms.Select(attrs={'class': 'form-select usuario-field', 'disabled': True}),
        }
