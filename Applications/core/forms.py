from django import forms
from .models import LandingPage, LandingSlide


class LandingPageForm(forms.ModelForm):
    class Meta:
        model = LandingPage
        fields = ['title', 'subtitle', 'background']
        labels = {
            'title': 'Título',
            'subtitle': 'Subtítulo',
            'background': 'Imagen de Fondo',
        }
        


class LandingSlideForm(forms.ModelForm):
    class Meta:
        model = LandingSlide
        fields = ['section', 'title', 'subtitle', 'content', 'image', 'order', 'active']
        labels = {
            'section': 'Sección',
            'title': 'Título',
            'subtitle': 'Subtítulo',
            'content': 'Contenido',
            'image': 'Imagen',
            'order': 'Orden',
            'active': 'Activo',
        }
        
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'maxlength': 150,
                'placeholder': 'Máximo 150 caracteres'
            }),
        }
        
        help_texts = {
            'content': 'Máximo 150 caracteres',
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        if len(content) > 150:
            raise forms.ValidationError('El contenido no puede exceder 150 caracteres.')
        return content
