from django import forms
from kiosco.models import *

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nombre",
            "apellido",
            "curso",
        ]
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'apellido':forms.TextInput(attrs={'class':'form-control'}),
            'curso':forms.Select(attrs={'class':'form-control'}),
        }

class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = [
            "codigo"
        ]
        widgets = {
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
        }

# class TarjetaUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Tarjeta
#         fields = [
#             "habilitada"
#         ]
#         widgets = {
#             'habilitada':forms.Select(attrs={'class':'form-control'}),
#         }

# class TarjetaSaldoForm(forms.ModelForm):
#     class Meta:
#         model = Tarjeta
#         fields = ["saldo"]
#         widgets = {
#             'saldo':forms.NumberInput(attrs={'class':'form-control'}),
#         }