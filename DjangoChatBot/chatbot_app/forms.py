from django import forms
from .models import PredefinedAnswer

class PredefinedAnswerForm(forms.ModelForm):
    keywords = forms.CharField(
        label='Palabras clave', 
        widget=forms.TextInput(attrs={'size': '30'})
    )
    answer = forms.CharField(
        label='Respuesta', 
        widget=forms.Textarea(attrs={'rows': 3})
    )
    class Meta:
        model = PredefinedAnswer
        fields = ['keywords', 'answer']