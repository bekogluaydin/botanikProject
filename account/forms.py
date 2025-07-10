from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User

from botanik_core.models import Collector, UserGroup, UserPermission
from botanik_core.utils.permissions import has_delete_permission

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



# User Group
class UserGroupCreateForm(forms.ModelForm):
    class Meta:
        model = UserGroup # Kullanıclacak olan model tanımlandı.

        #  fields = '__all__' # modeldeki tüm alanları ekler forma.
        fields = [
            "name", 
            "code", 
            "description", 
            "is_active"
        ] # modeldeki belirtilen alanları ekler forma

        labels = {
            'name': "Grup Adı",
            'code': "Grup Kodu",
            'description': "Grup Açıklaması",
            'is_active': "Grup Aktif mi?",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "code": forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class":"form-control", "cols": "40", "rows":"10"}),
            "isActive": forms.CheckboxInput(attrs={"class":"form-check-input"})
        }

        error_messages = {
            "name": {
                "required":"Grup Adı Boş Olamaz!"
            },
            "code": {
                "required":"Grup Kodu Boş Olamaz!"
            },
        }


class UserGroupEditForm(forms.ModelForm):
    class Meta:
        model = UserGroup # Kullanıclacak olan model tanımlandı.

        #  fields = '__all__' # modeldeki tüm alanları ekler forma.
        fields = [
            "name", 
            "code", 
            "description", 
            "is_active"
        ] # modeldeki belirtilen alanları ekler forma

        labels = {
            'name': "Grup Adı",
            'code': "Grup Kodu",
            'description': "Grup Açıklaması",
            'is_active': "Grup Aktif mi?",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "code": forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class":"form-control", "cols": "40", "rows":"10"}),
            "isActive": forms.CheckboxInput(attrs={"class":"form-check-input"})
        }

        error_messages = {
            "name": {
                "required":"Grup Adı Boş Olamaz!"
            },
            "code": {
                "required":"Grup Kodu Boş Olamaz!"
            },
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # request parametresi gelecek
        super().__init__(*args, **kwargs)

        if self.request and not has_delete_permission(self.request.user):
            self.fields["is_active"].disabled = True



# User Permission
class UserPermissionCreateForm(forms.ModelForm):
    class Meta:
        model = UserPermission

        fields = [
            "user",
            "can_view_tables",
            "can_add_tables",
            "deletion_permission",
            "user_group",
            "is_active"
        ]

        labels = {
            "user": "Kullanıcı",
            "can_view_tables": "Görebileceği Tablolar",
            "can_add_tables": "Kayıt Yapabileceği Tablolar",
            "deletion_permission": "Silme Yetkisi",
            "user_group": "Kullanıcı Grubu",
            "is_active": "Aktif mi?",
        }

        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "can_view_tables": forms.CheckboxSelectMultiple(),
            "can_add_tables": forms.CheckboxSelectMultiple(),
            "deletion_permission": forms.Select(attrs={"class": "form-select"}),
            "user_group": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

        error_messages = {
            "user": {"required": "Kullanıcı seçilmelidir!"},
            "user_group": {"required": "Kullanıcı grubu seçilmelidir!"},
        }


class UserPermissionEditForm(forms.ModelForm):
    class Meta:
        model = UserPermission
        exclude = ['user']  # user alanı forma eklenmesin

        fields = [
            "can_view_tables",
            "can_add_tables",
            "deletion_permission",
            "user_group",
            "is_active"
        ]

        labels = {
            "can_view_tables": "Görebileceği Tablolar",
            "can_add_tables": "Kayıt Yapabileceği Tablolar",
            "deletion_permission": "Silme Yetkisi",
            "user_group": "Kullanıcı Grubu",
            "is_active": "Aktif mi?",
        }

        widgets = {
            "can_view_tables": forms.CheckboxSelectMultiple(),
            "can_add_tables": forms.CheckboxSelectMultiple(),
            "deletion_permission": forms.Select(attrs={"class": "form-select"}),
            "user_group": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

        error_messages = {
            "user_group": {"required": "Kullanıcı grubu seçilmelidir!"},
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # request parametresi gelecek
        super().__init__(*args, **kwargs)

        if self.request and not has_delete_permission(self.request.user):
            self.fields["is_active"].disabled = True
    
    def clean_user(self):
        # Değişikliğe izin verme, her zaman orijinal kullanıcıyı geri döndür
        return self.instance.user
    


# Collector
class CollectorCreateForm(forms.ModelForm):
    class Meta:
        model = Collector

        fields = [
            "user", 
            "code",
            "phone",
            "is_active"
        ]

        labels = {
            "user": "Kullanıcı",
            "code": "Kodu",
            "phone": "Telefon",
            "is_active": "Aktif mi?",
        }

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

        error_messages = {
            "user": {"required": "Kullanıcı seçilmelidir!"},
            "code": {"required": "Kullanıcı Kodu boş olamaz!"},
        }


class CollectorEditForm(forms.ModelForm):
    class Meta:
        model = Collector
        exclude = ['user']  # user alanı forma eklenmesin

        fields = [
            "code",
            "phone",
            "is_active"
        ]

        labels = {
            "code": "Kodu",
            "phone": "Telefon",
            "is_active": "Aktif mi?",
        }

        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        error_messages = {
            "user": {"required": "Kullanıcı seçilmelidir!"},
            "code": {"required": "Kullanıcı Kodu boş olamaz!"},
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # request parametresi gelecek
        super().__init__(*args, **kwargs)

        if self.request and not has_delete_permission(self.request.user):
            self.fields["is_active"].disabled = True

    def clean_user(self):
        # Kullanıcı alanı disabled olduğu için POST'ta gelmez
        return self.instance.user
