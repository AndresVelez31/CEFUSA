# users/forms.py
from django import forms
from .models import Guardian, Player

class GuardianForm(forms.ModelForm):
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
        model = Guardian
        fields = '__all__'

class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.editable = kwargs.pop('editable', False)
        super().__init__(*args, **kwargs)

        # Etiquetas y textos de ayuda en español
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'document_type': 'Tipo de documento',
            'identification': 'Número de documento',
            'birth_date': 'Fecha de nacimiento',
            'birth_city': 'Ciudad de nacimiento',
            'address': 'Dirección',
            'city': 'Ciudad',
            'educational_institution': 'Institución educativa',
            'training_session': 'Jornada de entrenamiento',
            'has_disease': '¿Tiene alguna enfermedad?',
            'disease_type': 'Tipo de enfermedad',
            'has_contraindication': '¿Tiene contraindicación?',
            'emergency_contact': 'Contacto de emergencia',
            'contact_number': 'Número de contacto',
            'eps': 'EPS',
            'kinship': 'Parentesco',
            'health_center': 'Centro de atención',
            'pdf_doc_id': 'Documento de identidad (PDF)',
            'pdf_eps_certificate': 'Certificado EPS (PDF)',
            'fk_guardian': 'Acudiente',
        }
        placeholders = {
            'identification': 'Ingrese el número de documento del jugador.',
            'birth_date': 'Seleccione la fecha de nacimiento.',
            'educational_institution': 'Nombre de la institución educativa.',
            'disease_type': 'Especifique solo si tiene enfermedad.',
            'emergency_contact': 'Nombre del contacto de emergencia.',
            'contact_number': 'Teléfono del contacto de emergencia.',
            'pdf_doc_id': 'Suba el PDF del documento de identidad.',
            'pdf_eps_certificate': 'Suba el PDF del certificado de EPS.',
        }

        for field in self.fields.values():
            field.help_text = ''

        for field_name, field in self.fields.items():
            # Etiquetas en español
            if field_name in labels:
                field.label = labels[field_name]
            # Placeholder en español
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]

            # Widget especial para fecha de nacimiento
            if field_name == 'birth_date':
                field.widget = forms.DateInput(attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': placeholders.get('birth_date', '')
                }, format='%Y-%m-%d')
                field.input_formats = ['%Y-%m-%d']
            elif field_name in ['document_type', 'training_session', 'fk_guardian']:
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            if not self.editable and not self.instance._state.adding:
                if isinstance(field.widget, (forms.Select, forms.CheckboxInput)):
                    field.widget.attrs['disabled'] = True
                else:
                    field.widget.attrs['readonly'] = True

    class Meta:
        model = Player
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