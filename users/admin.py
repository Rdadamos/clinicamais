from django.contrib import admin
from .models import Attendant, Doctor, Patient

admin.site.register(Attendant)
admin.site.register(Doctor)
admin.site.register(Patient)
