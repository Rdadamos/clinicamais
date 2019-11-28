from django import forms
from .models import Appointment, DoctorSchedule

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('date', 'doctor', 'attendant', 'patient')
        widgets = {
            'date': forms.HiddenInput(),
            'doctor': forms.HiddenInput(),
            'attendant': forms.HiddenInput(),
            'patient': forms.HiddenInput(),
        }

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
