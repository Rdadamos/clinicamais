from django import forms
from .models import Attendant, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class AttendantForm(forms.ModelForm):
    class Meta:
        model = Attendant
        fields = ('name', 'phone', 'shift')
