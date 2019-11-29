from django.contrib import admin
from .models import Attendant, Doctor, Patient
from appointments.models import Appointment, DoctorSchedule, AppointmentExam, AppointmentMedicine
from medicines.models import Medicine
from exams.models import Exam

admin.site.register(Attendant)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(DoctorSchedule)
admin.site.register(AppointmentExam)
admin.site.register(AppointmentMedicine)
admin.site.register(Medicine)
admin.site.register(Exam)
