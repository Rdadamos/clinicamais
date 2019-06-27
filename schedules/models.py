from django.db import models
from users.models import Doctor

class Schedule(models.Model):
    date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
