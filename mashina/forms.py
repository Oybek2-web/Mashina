from django import forms
from .models import Mashina

class MashinaForms(forms.ModelForm):

    class Meta:
        model = Mashina
        fields = '__all__'