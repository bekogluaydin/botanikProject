from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Collector(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=False, null=False, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"