from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Collector(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.id} - {self.name} {self.surname} ({self.code})"


class AccessionRecord(models.Model):
    accession_number = models.CharField(max_length=10, unique=True, blank=True)
    taxon_name = models.CharField(max_length=100)
    material_type = models.CharField(max_length=50)
    origin = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=50, blank=True, null=True)
    collection_date = models.DateField(blank=True, null=True)
    collector = models.ForeignKey('Collector', on_delete=models.PROTECT) # Collector her şekilde eklenmeli boş bırakılmamalı.Eğer Collector bilgisi yok ise sistemde varsayılan bir kullanıcı olmalı Collectoru belli olmayanlar o varsyılan kişiye atanmalı otomatik olarak.
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Kullanıcı accession_number elle girdiyse kullan fakat kullanmadan önce kontrol et.
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
        return f"{self.accession_number} ({self.taxon_name})"


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
    collector = models.ForeignKey('Collector', on_delete=models.PROTECT) # Toplayıcı tablosu  ad, kod ve no için. Collector her şekilde eklenmeli boş bırakılmamalı. Eğer Collector bilgisi yok ise sistemde varsayılan bir kullanıcı olmalı Collectoru belli olmayanlar o varsyılan kişiye atanmalı otomatik olarak.
    photo = models.ImageField(upload_to='herbarium_photos/', default="", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accession.accession_number} - {self.herbarium_number}"


class GardenLocation(models.Model):
    name = models.CharField(max_length=100)  # Örn: Merkez Ada
    sub_location = models.CharField(max_length=100, blank=True, null=True)  # Örn: Üst Gölet

    island_code = models.PositiveSmallIntegerField()  # Örn: 1
    sub_code = models.CharField(max_length=10)  # Örn: ÜG (Üst Gölet), BB (Bataklık Bölümü)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}; {self.sub_location or 'Alt Bölüm Yok'} ({self.location_code or 'Yer Kodu Yok'})"

    @property #Python’da bir sınıf (class) içinde fonksiyon gibi çalışan ama dışarıdan alan gibi erişilen yapıdır. "kayit.name" ile ilgili kaydın tabloda ki name alanına erişebiliyoruz "kayit.location_code" da aynı mantıkla çalışıyor @property yazdığımızda.
    def location_code(self):
        return f"{self.island_code}-{self.sub_code}"


class PlantStatusRecord(models.Model):
    accession = models.ForeignKey('AccessionRecord', on_delete=models.PROTECT)
    status_date = models.DateField()
    garden_location = models.ForeignKey('GardenLocation', on_delete=models.PROTECT)
    status = models.CharField(max_length=100)
    vegetative_state = models.CharField(max_length=100, blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accession.accession_number} ({self.accession.taxon_name}) - {self.status} ({self.status_date})"


class TablePermissionArea(models.Model): # Veri tabanındaki tabloları temsil eder (örnek: Herbaryum, Tohum Bankası)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "İzin Verilecek Tablo (TablePermissionArea)"
        verbose_name_plural = "İzin Verilecek Tablolar (TablePermissionArea)"

    def __str__(self):
        return self.name


class DeletionPermissionChoices(models.TextChoices):
    NO = "no", "Hayır"
    YES = "yes", "Evet"
    WITH_APPROVAL = "with_approval", "Yönetici Onayıyla"


class UserGroup(models.Model):
    name = models.CharField(max_length=50, unique=True) # Örnek: "Sistem Yöneticisi"
    code = models.CharField(max_length=20, unique=True) # Örnek: "ADMIN"
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kullanıcı Grubu (UserGroup)"
        verbose_name_plural = "Kullanıcı Grupları (UserGroup)"

    def __str__(self):
        return f"{self.name} - {self.code}"


class UserPermission(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    can_view_tables = models.ManyToManyField(
        TablePermissionArea,
        related_name="viewable_by_users",
        blank=True
    )
    can_add_tables = models.ManyToManyField(
        TablePermissionArea,
        related_name="addable_by_users",
        blank=True
    )

    deletion_permission = models.CharField(
        max_length=20,
        choices=DeletionPermissionChoices.choices,
        default=DeletionPermissionChoices.NO
    )

    user_group = models.OneToOneField(UserGroup, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Kullanıcı Yetkisi (UserPermission)"
        verbose_name_plural = "Kullanıcı Yetkileri (UserPermission)"

    def __str__(self):
        return self.user.username

    def view_tables_list(self): # Görebileceği tablolar için many-to-many ilişkisi kurulduğu için tek seferlik böyle bir kod yazdık. Her seferinde yazmamk adına. Tek yapılması gereken kayit.view_tables_list()
        return ", ".join([table.name for table in self.can_view_tables.all()])
    view_tables_list.short_description = "Görebileceği Tablolar"

    def add_tables_list(self):
        return ", ".join([table.name for table in self.can_add_tables.all()])
    add_tables_list.short_description = "Kayıt Yapabileceği Tablolar"