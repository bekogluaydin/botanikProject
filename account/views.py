from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from account.forms import CustomUserCreationForm, CustomUserPasswordChangeForm, LoginUserForm, UserGroupCreateForm, UserGroupEditForm
from botanik_core.models import TablePermissionArea, UserGroup

def user_login(request):
    if request.user.is_authenticated:
        # return redirect("home")  # varsa ana sayfaya yönlendir
        # return redirect("/admin/")
        return render(request, "base.html")

    
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                messages.add_message(request, messages.SUCCESS, "Giriş başarılı.")

                return render(request, "base.html")
                # return redirect("home")
                # return redirect("/admin/")
            
            else:
                messages.add_message(request, messages.ERROR, "There was a problem with the login process.")
                return render(request, "account/login.html", {"form":form})

        else:
            messages.add_message(request, messages.ERROR, "There was a problem with the login process.")
            return render(request, "account/login.html", {"form":form})

    else:
        form = LoginUserForm()
        return render(request, "account/login.html", {"form": form})


def user_register(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.SUCCESS, "Zaten giriş yaptınız. Kayıt sayfasına ulaşamazsınız.")
        return render(request, "base.html")
   
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.add_message(request, messages.SUCCESS, "Kayıt işlemi tamamlandı ve giriş yapıldı.")

            return redirect("account:user_login")
        
            # return redirect("home")

        else:
            messages.add_message(request, messages.ERROR, "Kayıt işleminde bir sorun oluştu.")
            return render(request, "account/register.html", {"form": form})
    
    else:
        form = CustomUserCreationForm()
        return render(request, "account/register.html", {"form": form})


@login_required
def user_change_password(request):
    if request.method == "POST":
        form = CustomUserPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            messages.add_message(request, messages.SUCCESS, "Şifre Güncellendi.")

            # return redirect("home")
            return render(request, "base.html")
        
        else:
            messages.add_message(request, messages.WARNING, "Şifre Güncellenmedi.")
            return render(request, "account/change-password.html", {"form": form})

    form = CustomUserPasswordChangeForm(request.user)
    return render(request, "account/change-password.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Çıkış Yapıldı.")
    return redirect("account:user_login")


# User Group
@login_required
def user_group_list(request):
    user_groups_list = UserGroup.objects.all()
    return render(request, "account/user_group/user_group_list.html", {
        "groups": user_groups_list
    })


@login_required
def user_group_create(request):

    if request.method == "POST":
        form = UserGroupCreateForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("account:user_group_list")
    else:
        form = UserGroupCreateForm()

    return render(request, "account/user_group/user_group_create.html", {"form": form})


@login_required
def user_group_edit(request, user_group_id):
    get_user_group = get_object_or_404(UserGroup, pk=user_group_id)

    if request.method == "POST":
        form = UserGroupEditForm(request.POST, instance=get_user_group) # ilk iki parametre formdan gelen, instance parametresi ise DB'den gelen. İkisi karşılaştırılır Formdan gelen hangi alanlarda farklılık varsa sadece onlar için form.save() çalışır. Değişmeyen bilgilerde güncelleme yapılmaz.
        
        if form.is_valid():
            form.save()
            return redirect("account:user_group_list")
    else:
        form = UserGroupEditForm(instance=get_user_group)

    return render(request, "account/user_group/user_group_edit.html", {"form": form})


def user_group_delete(request, user_group_id):
    get_user_group = get_object_or_404(UserGroup, pk=user_group_id)

    if request.method == "POST":
        get_user_group.is_active = False
        get_user_group.save()
        
        return redirect(reverse('account:user_group_list'))
    
    return render(request, "account/user_group/user_group_delete.html", {
        'user_group': get_user_group
    })


# Table Permission Area
@login_required
def table_permission_area_list(request):
    table_permission_area_list = TablePermissionArea.objects.all()
    return render(request, "account/table_permission_area/table_permission_area_list.html", {
        "table_permissions": table_permission_area_list
    })