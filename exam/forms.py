from django import forms
from django.core.exceptions import ValidationError
from .models import *

class MaterieForm(forms.ModelForm):
    class Meta:
        model = Materie
        fields = ['titlu', 'durata_ore', 'profesor']
    
    def clean(self):
        cleaned_data = super().clean()
        titlu = cleaned_data.get('titlu')
        durata_ore = cleaned_data.get('durata_ore')
        
        materiiSimilare = Materie.objects.filter(titlu__iexact = titlu)
        if len(materiiSimilare) > 0:
            raise forms.ValidationError('Titlul trebuie sa fie unic!')
        if durata_ore < 5 or durata_ore > 50:
            raise forms.ValidationError('Durata trebuie sa fie cuprinsa intre 5 si 50 de ore')
        return cleaned_data