from django import forms
from botanik_core.models import AccessionRecord

class AccessionRecordForm(forms.ModelForm):
    class Meta:
        model = AccessionRecord
        fields = [
            "accession_number",  # Kullanıcı isterse elle girsin, boşsa otomatik oluşacak
            "taxon_name",
            "material_type",
            "origin",
            "location",
            "coordinates",
            "note",
            "collection_date",
        ]

        labels = {
            "accession_number": "Aksesyon Numarası (Boş bırakılırsa otomatik atanır)",
            "taxon_name": "Bitki Ad",
            "material_type": "Materyal Türü",
            "origin": "Köken",
            "location": "Lokasyonu",
            "coordinates": "Koordinat",
            "note": "Not",
            "collection_date": "Toplanma Tarihi",
        }

        widgets = {
            "accession_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Boş bırakırsanız otomatik oluşturulur."}),
            "taxon_name": forms.TextInput(attrs={"class": "form-control"}),
            "material_type": forms.TextInput(attrs={"class": "form-control"}),
            "origin": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "coordinates": forms.TextInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(attrs={"class":"form-control", "cols": "40", "rows":"10"}),
            "collection_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    error_messages = {
            "taxon_name": {
                "required":"Bitki Adı Boş Olamaz!"
            },
            "material_type": {
                "required":"Materyal Çeşidi Boş Olamaz!"
            },
            "origin": {
                "required":"Köken Boş Olamaz!"
            },
            "collector": {
                "required":"Toplayıcı Boş Olamaz!"
            },
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
