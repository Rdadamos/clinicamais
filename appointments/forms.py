from django import forms
from .models import DoctorSchedule

class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ('available', 'hour', 'day', 'doctor')
        labels = {
            'available': ''
        }
        widgets = {
            'hour': forms.HiddenInput(),
            'day': forms.HiddenInput(),
            'doctor': forms.HiddenInput()
        }
