from django.urls import path
from . import views

app_name = "accession_record"

urlpatterns = [
    # User Group
    path("accession-record/", views.accession_list, name="accession_list"),
    path("accession-record/create/", views.accession_create, name="accession_create"),
    path('accession-record/edit/<int:accession_id>', views.accession_edit, name='accession_edit'),
    path('accession-record/delete/<int:accession_id>', views.accession_delete, name='accession_delete'),
]