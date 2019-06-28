from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=11, default='')

    class Meta:
        abstract = True

class Doctor(User):
    speciality = models.CharField(max_length=255)

class Attendant(User):
    SHIFTS = [
        ('M', 'Manhã'),
        ('T', 'Tarde'),
        ('I', 'Integral'),
    ]
    shift = models.CharField(max_length=1, choices=SHIFTS, default='I')

class Patient(User):
    birthdate = models.DateField()
    GENDER = [
        ('H', 'Homem'),
        ('M', 'Mulher'),
        ('O', 'Outro'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER, default='H')
