from django.db import models
from users.models import Doctor, Attendant, Patient
from exams.models import Exam
from medicines.models import Medicine
import datetime as datetime

class Appointment(models.Model):
    date = models.DateTimeField()
    prescription = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    attendant = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

class AppointmentExam(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    result = models.TextField()

class AppointmentMedicine(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=255)

class DoctorSchedule(models.Model):
    day = models.IntegerField()
    hour = models.TimeField()
    available = models.BooleanField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('doctor', 'day', 'hour',)
