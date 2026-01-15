from django import forms
from productos.models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "marca",
            "categoria",
            "precio",
            "stock",
            "codigo_de_barras",
            "picture"
        ]
        widgets = {
            'picture': forms.FileInput(attrs={"class": "form-control"}),
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'marca':forms.TextInput(attrs={'class':'form-control'}),
            'categoria':forms.Select(attrs={'class':'form-control'}),
            'precio':forms.NumberInput(attrs={'class':'form-control'}),
            'stock':forms.NumberInput(attrs={'class':'form-control'}),
            'codigo_de_barras':forms.TextInput(attrs={'class':'form-control'}),
        }
