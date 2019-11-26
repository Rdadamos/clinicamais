from django.contrib import admin
from .models import Attendant, Doctor, Patient
from appointments.models import DoctorSchedule

admin.site.register(Attendant)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(DoctorSchedule)
