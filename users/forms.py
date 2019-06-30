from django import forms
from django.forms.widgets import DateInput
from django.contrib.admin.widgets import AdminDateWidget
from .models import Attendant, Doctor, Patient, User


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

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('name', 'phone', 'speciality')
        labels = {
            'name': 'Nome',
            'phone': 'Telefone',
            'speciality': 'Especialidade'
        }
        help_texts = {
            'name': 'Nome completo',
            'phone': 'Digite somente os números',
            'speciality': 'Especialidade médica'
        }

class PatientForm(forms.ModelForm):
    # birthdate = DateField(widget=AdminDateWidget)
    class Meta:
        model = Patient
        fields = ('name', 'phone', 'birthdate', 'gender')
        labels = {
            'name': 'Nome',
            'phone': 'Telefone',
            'birthdate': 'Nascimento',
            'gender': 'Sexo'
        }
        help_texts = {
            'name': 'Nome completo',
            'phone': 'Digite somente os números',
            'birthdate': 'Data de nascimento'
        }
        widgets = {
            'birthdate': DateInput(attrs={'type':'date'})
        }
