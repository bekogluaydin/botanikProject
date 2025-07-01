from django.contrib import admin

# Register your models here.
from .models import (
    Collector,
    AccessionRecord,
    SeedBankRecord,
    HerbariumRecord,
    GardenLocation,
    PlantStatusRecord
    )


@admin.register(Collector)
class CollectorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "surname",
        "code",
        "phone",
        "email",
        "is_active"
    )

    search_fields = (
        "name",
        "surname",
        "code",
        "phone",
        "email",
    )

    list_filter = ("is_active",)


@admin.register(AccessionRecord)
class AccessionRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "accession_number",
        "taxon_name",
        "material_type",
        "origin",
        "location",
        "collection_date",
        "collector",
        "created_at"
    )

    search_fields  = (
        "accession_number",
        "taxon_name",
        "material_type",
        "origin",
        "location",
        "collection_date",
        "collector__name",
        "collector__surname",
        "collector__code"
    )

    list_filter = (
        "material_type",
        "origin",
        "location",
        "coordinates",
        "collection_date",
    )

    autocomplete_fields = ("collector",) # Yüzlerce kayıt varsa ForeignKey alanlarını otomatik arama ile getirir.


@admin.register(SeedBankRecord)
class SeedBankRecordAdmin(admin.ModelAdmin):
    list_display = (
        "accession",
        "accession__collector",
        "quantity_description",
        "storage_location",
        "storage_date",
        "created_at",
    )

    search_fields = (
        "accession__accession_number",
        "accession__taxon_name",
        "accession__material_type",
        "accession__origin",
        "accession__collector__name",
        "accession__collector__surname",
        "accession__collector__code",
        "quantity_description",
        "storage_location",
        "storage_date"
    )

    list_filter = (
        "accession__taxon_name",
        "accession__material_type",
        "accession__origin",
        "storage_location",
        "storage_date"
    )

    autocomplete_fields = ("accession",)


@admin.register(HerbariumRecord)
class HerbariumRecordAdmin(admin.ModelAdmin):
    list_display = (
        "herbarium_number",
        "accession",
        "collector",
        "accession__location",
        "accession__coordinates",
        "photo",
        "created_at"
    )

    search_fields = (
        "herbarium_number",
        "accession__accession_number",
        "accession__taxon_name",
        "accession__material_type",
        "accession__origin",
        "collector__name",
        "collector__surname",
        "collector__code",
        "accession__location",
    )

    list_filter = (
        "accession__taxon_name",
        "accession__material_type",
        "accession__origin",
        "accession__location",
        "accession__coordinates",
    )

    autocomplete_fields = ("accession", "collector")


@admin.register(GardenLocation)
class GardenLocationAdmin(admin.ModelAdmin):
    list_display = (
    "id",
    "name",
    "sub_location",
    "island_code",
    "sub_code",
    "location_code",
    "is_active",
    "created_at"
    )

    search_fields = (
        "name",
        "sub_location",
        "island_code",
        "sub_code",
        "location_code",
        "is_active"
    )

    list_filter = (
        "name",
        "island_code",
        "is_active"
    )


@admin.register(PlantStatusRecord)
class PlantStatusRecordAdmin(admin.ModelAdmin):
    list_display = (
        "accession",
        "status_date",
        "garden_location",
        "status",
        "vegetative_state",
        "observation",
        "created_at"
    )

    search_fields = (
        "accession__accession_number",
        "accession__taxon_name",
        "accession__material_type",
        "accession__origin",
        "status_date",
        "garden_location",
        "status",
        "vegetative_state",
        "observation"
    )

    list_filter = (
        "accession__taxon_name",
        "accession__material_type",
        "accession__origin",
        "status_date",
        "garden_location",
        "status",
        "vegetative_state",
    )

    autocomplete_fields = ("accession", "garden_location")