from django import forms
from kiosco.models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "marca",
            "categoria",
            "precio",
            "stock",
            "codigo_de_barras"
        ]
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'marca':forms.TextInput(attrs={'class':'form-control'}),
            'categoria':forms.TextInput(attrs={'class':'form-control'}),
            'precio':forms.NumberInput(attrs={'class':'form-control'}),
            'stock':forms.NumberInput(attrs={'class':'form-control'}),
            'codigo_de_barras':forms.TextInput(attrs={'class':'form-control'}),
        }

class AlumnaForm(forms.ModelForm):
    class Meta:
        model = Alumna
        fields = [
            "nombre",
            "apellido",
            "curso",
        ]
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'apellido':forms.TextInput(attrs={'class':'form-control'}),
            'curso':forms.TextInput(attrs={'class':'form-control'}),
        }

class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = [
            "codigo",
        ]
        widgets = {
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
        }