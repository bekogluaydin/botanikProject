from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User

class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.fields["username"].widget = forms.widgets.TextInput(attrs={'class': 'form-control'})
        self.fields["password"].widget = forms.widgets.PasswordInput(attrs={'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if username != "admin":
            messages.add_message(self.request, messages.SUCCESS, "Welcome admin")

            return username

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget = forms.widgets.TextInput(attrs={'class': 'form-control'})
        self.fields["last_name"].widget = forms.widgets.TextInput(attrs={'class': 'form-control'})
        self.fields["username"].widget = forms.widgets.TextInput(attrs={'class': 'form-control'})
        self.fields["email"].widget = forms.widgets.EmailInput(attrs={'class': 'form-control'})
        self.fields["email"].required = True
        self.fields["password1"].widget = forms.widgets.PasswordInput(attrs={'class': 'form-control'})
        self.fields["password2"].widget = forms.widgets.PasswordInput(attrs={'class': 'form-control'})

    def clean_email(self): # clean_xXx başına clean eklediğimizde istediğimiz property'i kontrol edebiliyoruz.

        form_email = self.cleaned_data.get("email")

        if User.objects.filter(email=form_email).exists():
            # add_error da ilk parametre hata mesajının formda ki hangi inputun üstünde çıkacağını belirler. Biz email ile alakalı olduğu için email dedik. Fakat istedğimiz form eleman adını yazabiliriz.
            self.add_error("email", "A user with that email already exists.")  

        return form_email

class CustomUserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].widget = forms.widgets.PasswordInput(attrs={'class': 'form-control'})
        self.fields["new_password1"].widget = forms.widgets.PasswordInput(attrs={'class': 'form-control'})
        self.fields["new_password2"].widget = forms.widgets.PasswordInput(attrs={'class': 'form-control'})