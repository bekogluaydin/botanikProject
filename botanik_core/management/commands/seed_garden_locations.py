from django.core.management.base import BaseCommand
from botanik_core.models import GardenLocation

class Command(BaseCommand):
    help = "Seed GardenLocation data"

    def handle(self, *args, **options):
        data = [
            {"name": "Merkez Ada", "sub_location": "Üst Gölet Alanı", "island_code": 1, "sub_code": "ÜG"},
            {"name": "Merkez Ada", "sub_location": "Soğanlı Bitkiler Alanı", "island_code": 1, "sub_code": "SB"},

            {"name": "Ertuğrul Adası", "sub_location": "Bataklık Bölümü", "island_code": 2, "sub_code": "BB"},
            {"name": "Ertuğrul Adası", "sub_location": "Japon Sakura Bölümü", "island_code": 2, "sub_code": "JSB"},

            {"name": "Mesire Adası", "sub_location": "Keşif Bahçesi Alanı", "island_code": 3, "sub_code": "KB"},
            {"name": "Mesire Adası", "sub_location": "Bambu Labirent Alanı", "island_code": 3, "sub_code": "BL"},

            {"name": "İstanbul Adası", "sub_location": "Eski Konak Bahçesi", "island_code": 4, "sub_code": "EKB"},
            {"name": "İstanbul Adası", "sub_location": "Boğaziçi Kanalı", "island_code": 4, "sub_code": "BK"},

            {"name": "Arboretum Adası", "sub_location": "Mini Kaya Bahçesi", "island_code": 5, "sub_code": "MK"},

            {"name": "Meşe Adası", "sub_location": "Meşe Bendi Tortu Gölet", "island_code": 6, "sub_code": "MBTG"},

            {"name": "Anadolu Adası", "sub_location": "Kaya Bahçesi", "island_code": 7, "sub_code": "KB"},
            {"name": "Anadolu Adası", "sub_location": "Sulak Vadi", "island_code": 7, "sub_code": "SV"},

            {"name": "Trakya Adası", "sub_location": "Meyve Koleksiyonu", "island_code": 8, "sub_code": "MK"},
            {"name": "Trakya Adası", "sub_location": "Kumul Koruma Alanı", "island_code": 8, "sub_code": "KK"},
        ]

        created = 0
        for item in data:
            obj, is_created = GardenLocation.objects.get_or_create(
                name=item["name"],
                sub_location=item["sub_location"],
                defaults={
                    "island_code": item["island_code"],
                    "sub_code": item["sub_code"],
                }
            )
            if is_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"{created} GardenLocation kaydı eklendi."))