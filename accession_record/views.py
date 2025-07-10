# accession_record/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from botanik_core.utils.permissions import has_delete_approval_required, has_delete_permission, has_permission_to_view, has_permission_to_add
from botanik_core.models import Collector, AccessionRecord
from botanik_core.utils.permissions import has_permission_to_view
from .forms import AccessionRecordForm


@login_required
def accession_list(request):
    if not has_permission_to_view(request.user, "AccessionRecord"):
        messages.add_message(request, messages.ERROR, "Bu sayfaya erişim yetkiniz bulunmamaktadır. Ana Sayfaya yönlendirildiniz.")
        
        return redirect("botanik_core:home_page")

    records = AccessionRecord.objects.filter().order_by("-created_at")
    return render(request, "accession_record/list.html", {
        "records": records
    })


@login_required
def accession_create(request):
    if not has_permission_to_add(request.user, "AccessionRecord"):
        messages.add_message(request, messages.ERROR, "Bu tabloya kayıt ekleme yetkiniz bulunmamaktadır. Ana Sayfaya yönlendirildiniz.")

        return redirect("botanik_core:home_page")

    # Collector kontrolü – kullanıcıya ait Collector kaydı yoksa oluştur
    collector, created = Collector.objects.get_or_create(user=request.user, defaults={
        "name": request.user.first_name or "İsimsiz",
        "surname": request.user.last_name or "Kullanıcı",
        "code": f"{request.user.username.upper()}-CL",  # örnek bir collector code
        "phone": "",
        "email": request.user.email,
        "is_active": True,
    })

    form = AccessionRecordForm(request.POST or None)

    if form.is_valid():
        record = form.save(commit=False)
        record.collector = collector  # Collector'ı buraya bağla
        record.save()

        messages.add_message(request, messages.SUCCESS, "Aksesyon Oluşturuldu.")
        return redirect("accession_record:accession_list")

    return render(request, "accession_record/create.html", {"form": form})


@login_required
def accession_edit(request, accession_id):
    if not has_permission_to_add(request.user, "AccessionRecord"):
        messages.add_message(request, messages.ERROR, "Bu sayfaya erişim yetkiniz bulunmamaktadır. Ana Sayfaya yönlendirildiniz.")
        
        return redirect("botanik_core:home_page")

    get_accession = get_object_or_404(AccessionRecord, pk=accession_id)

    if request.method == "POST":
        form = AccessionRecordForm(request.POST, instance=get_accession, request=request) # ilk iki parametre formdan gelen, instance parametresi ise DB'den gelen. İkisi karşılaştırılır Formdan gelen hangi alanlarda farklılık varsa sadece onlar için form.save() çalışır. Değişmeyen bilgilerde güncelleme yapılmaz.
        
        if form.is_valid():
            form.save()
            return redirect("accession_record:accession_list")
    else:
        form = AccessionRecordForm(instance=get_accession, request=request)

    return render(request, "accession_record/edit.html", {"form": form})


def accession_delete(request, accession_id):
    get_accession = get_object_or_404(AccessionRecord, pk=accession_id)

    if not has_permission_to_view(request.user, "AccessionRecord"):  # opsiyonel kontrol
        messages.error(request, "Bu işlemi görüntüleme yetkiniz yok.")
        return redirect("botanik_core:home_page")
    
    if not has_delete_permission(request.user):
        if has_delete_approval_required(request.user):
            messages.warning(request, "Bu silme işlemi için yönetici onayı gerekmektedir.")
        else:
            messages.error(request, "Bu silme işlemi için yetkiniz bulunmamaktadır.")
        return redirect("account:collector_list")

    if request.method == "POST":
        get_accession.is_active = False
        get_accession.save()
        
        messages.add_message(request, messages.SUCCESS, "Kayıt başarıyla pasif hale getirildi.")
        return redirect(reverse('accession_record:accession_list'))
    
    return render(request, "accession_record/delete.html", {
        "record": get_accession
    })
