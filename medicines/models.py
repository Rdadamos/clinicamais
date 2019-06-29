from django.db import models

class Medicine(models.Model):
    generic_name = models.CharField(max_length=255)
    factory_name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
