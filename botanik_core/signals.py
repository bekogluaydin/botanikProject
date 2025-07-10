from django.db.models.signals import post_migrate
from django.apps import apps
from django.dispatch import receiver
from .models import TablePermissionArea

# Tabloya otomatik eklenmesini istemediğimiz modelleri/tabloları "BLACKLISTED_MODELS" array içinde belirtiyoruz.
BLACKLISTED_MODELS = [
    'LogEntry',
    'Session',
    'ContentType',
    'Permission',
    'Group',
    'User',
    'UserGroup',
    'UserPermission'
]

@receiver(post_migrate)
def populate_permission_areas(sender, **kwargs):
    existing_names = set(TablePermissionArea.objects.values_list("name", flat=True)) # TablePermissionArea tablosunda ki kayıtları "existing_names" adında ki listeye eşitledik.

    # existing_names listesi kontrol ediliyor eğer bu tablo eklenmişse bir işlem yapmıyor. Tablo yoksa liste içinde "TablePermissionArea" tablosuna ilgili eklenmemiş tabloları ekliyoruz.
    for model in apps.get_models():
        model_name = model.__name__
        if model_name in BLACKLISTED_MODELS:
            continue
        if model_name not in existing_names:
            TablePermissionArea.objects.create(name=model_name)