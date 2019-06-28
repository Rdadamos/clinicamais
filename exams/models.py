from django.db import models

class Exam(models.Model):
    name = models.CharField(max_length=255)
