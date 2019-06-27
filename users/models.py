from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

class Attendant(User):
    company = models.CharField(max_length=255)

class Doctor(User):
    speciality = models.CharField(max_length=255)

class Patient(User):
    phone = models.CharField(max_length=13)
