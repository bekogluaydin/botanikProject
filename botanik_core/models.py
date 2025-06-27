from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class Collector(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
    

class AccessionRecord(models.Model):
    accession_number = models.CharField(max_length=10, unique=True, blank=True)
    taxon_name = models.CharField(max_length=100)
    material_type = models.CharField(max_length=50)
    origin = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=50, blank=True, null=True)
    collection_date = models.DateField()
    collector = models.ForeignKey('Collector', on_delete=models.PROTECT)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If the user entered the access_number manually use it, but check it
        if self.accession_number:
            if AccessionRecord.objects.filter(accession_number=self.accession_number).exclude(pk=self.pk).exists():
                raise ValidationError(f"accession_number zaten var. Lütfen numarayı kontrol edin: {self.accession_number}")
        
        else:
            # Otomatik accession_number üret
            year = timezone.now().year
            count = AccessionRecord.objects.filter(accession_number__startswith=f"{year}-").count() + 1
            number = str(count).zfill(5) # 5 karakter olcak. Örneğin count 15 çıktı bu durumda 00015 olacak. Count 5789 çıkarsa bu sefer 05789. Karakteri 0 lar ile 5 tamamlıyor.
            generated_number = f"{year}-{number}"

            # Son kontrol - Nadirde olsa çakışma olabilir
            while AccessionRecord.objects.filter(accession_number=generated_number).exists():
                count += 1
                number = str(count).zfill(5)
                generated_number = f"{year}-{number}"
            self.accession_number = generated_number

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.accession_number} - {self.taxon_name}"
    

class SeedBankRecord(models.Model):
    accession = models.ForeignKey('AccessionRecord', on_delete=models.PROTECT)
    quantity_description = models.TextField(max_length=200)
    storage_location = models.CharField(max_length=50)
    storage_date = models.DateField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accession.accession_number} - {self.accession.taxon_name} - Tohum Kaydı"
    

class HerbariumRecord(models.Model):
    herbarium_number = models.CharField(max_length=50, unique=True) # proje isterlerinde her numuneye özel bir herbaryum no olup olmadığı yazmıyor. Aynı zamanda görsele baktığımızda örneğin 345 numaralı kayıt 1 kez var. Birden fazla var mı belli değil. Bu yüzden "unique=True" olarak belirttim.
    accession = models.ForeignKey('AccessionRecord', on_delete=models.PROTECT) # Aksesyon Defter tablosu bitki adı, lokasyon, koordinat ve aksesyon no için
    collector = models.ForeignKey('Collector', on_delete=models.PROTECT) # Toplayıcı tablosu  ad, kod ve no için.
    photo = models.ImageField(upload_to='herbarium_photos/', default="", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accession.accession_number} - {self.herbarium_number}"