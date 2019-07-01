from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, default='')

    class Meta:
        abstract = True

class Doctor(Profile):
    speciality = models.CharField(max_length=255)

class Attendant(Profile):
    SHIFTS = [
        ('I', 'Integral'),
        ('M', 'Manhã'),
        ('T', 'Tarde'),
    ]
    shift = models.CharField(max_length=1, choices=SHIFTS, default='I')

class Patient(Profile):
    birthdate = models.DateField()
    GENDER = [
        ('H', 'Homem'),
        ('M', 'Mulher'),
        ('O', 'Outro'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER, default='H')
