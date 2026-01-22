from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import Perfil

class PerfilCreateForm(UserCreationForm):
    class Meta:
        model = Perfil
        fields = ("first_name","last_name", "username", "email")

        widgets = {
            "first_name":forms.TextInput(attrs={'autofocus': True, "class": "form-control"}),
            "last_name":forms.TextInput(attrs={"class": "form-control"}),
            "username":forms.TextInput(attrs={"class": "form-control"}),
            "email":forms.EmailInput(attrs={"class": "form-control"}),
            "celular":forms.NumberInput(attrs={"class": "form-control"}),
        }
    
class PerfilChangeForm(UserChangeForm):
    class Meta:
        model = Perfil
        fields = ("avatar", "direccion", "celular", "first_name", "last_name", "email")

        widgets = {
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "email":forms.EmailInput(attrs={"class": "form-control"}),
            "celular":forms.NumberInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }