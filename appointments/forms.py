from django import forms
from .models import Appointment,AppointmentExam, AppointmentMedicine, DoctorSchedule
from exams.models import Exam
from medicines.models import Medicine

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

class AppointmentInProgressForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = {'prescription', 'attended'}
        labels = {
            'prescription': 'Prescrição',
            'attended': ''
        }
        widgets = {
            'prescription': forms.Textarea(attrs={'placeholder': 'Preencher'}),
            'attended': forms.HiddenInput()
        }

class CustomMedicineChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s (%s)" % (obj.factory_name, obj.generic_name)

class AppointmentMedicineForm(forms.ModelForm):
    medicine = CustomMedicineChoiceField(queryset=Medicine.objects.all(), label="Medicamento")
    class Meta:
        model = AppointmentMedicine
        fields = ('medicine', 'dosage', 'appointment')
        labels = {
            'dosage': 'Dosagem',
            'appointment': ''
        }
        widgets = { 'appointment': forms.HiddenInput() }

class CustomExamChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class AppointmentExamForm(forms.ModelForm):
    exam = CustomExamChoiceField(queryset=Exam.objects.all(), label="Exame")
    class Meta:
        model = AppointmentExam
        fields = ('exam', 'appointment')
        labels = { 'appointment': '' }
        widgets = { 'appointment': forms.HiddenInput() }
