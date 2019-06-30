from django import forms
from .models import Attendant, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        labels = {
            'email': 'E-mail',
            'password': 'Senha'
        }
        help_texts = {
            'username': 'Para ser utilizado no login',
            'email': 'Digite um e-mail válido'
        }
        widgets = {
            'password': forms.PasswordInput()
        }

class AttendantForm(forms.ModelForm):
    class Meta:
        model = Attendant
        fields = ('name', 'phone', 'shift')
        labels = {
            'name': 'Nome',
            'phone': 'Telefone',
            'shift': 'Turno'
        }
        help_texts = {
            'name': 'Nome completo',
            'phone': 'Digite somente os números',
            'shift': 'Informe o turno'
        }
