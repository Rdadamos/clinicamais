from django.contrib import admin
from .models import Attendant, Doctor, Patient
from appointments.models import Appointment, DoctorSchedule

admin.site.register(Attendant)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(DoctorSchedule)
