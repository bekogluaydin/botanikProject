from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from account.forms import CustomUserCreationForm, CustomUserPasswordChangeForm, LoginUserForm

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
        
            # return redirect("course_list")

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

            # return redirect("course_list")
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