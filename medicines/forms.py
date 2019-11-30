from django import forms
from django.forms.widgets import DateInput
from .models import Medicine


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ('generic_name', 'factory_name', 'manufacturer')
        labels = {
            'generic_name': 'Nome genérico',
            'factory_name': 'Nome de fábrica',
            'manufacturer': 'Fabricante'
        }
