from django import forms
from .models import LandingPage, LandingSlide


class LandingPageForm(forms.ModelForm):
    class Meta:
        model = LandingPage
        fields = ['title', 'subtitle', 'background']


class LandingSlideForm(forms.ModelForm):
    class Meta:
        model = LandingSlide
        fields = ['section', 'title', 'subtitle', 'content', 'image', 'order', 'active']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
