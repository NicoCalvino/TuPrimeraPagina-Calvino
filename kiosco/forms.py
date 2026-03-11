from django import forms
from kiosco.models import *

class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = [
            "codigo"
        ]
        widgets = {
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
        }

class TarjetasMasivoForm(forms.Form):
    numero_desde = forms.IntegerField(
        label='Número Desde',
        required=True,
        min_value=1,
        max_value=999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', # <-- ESTO ES CLAVE PARA EL DISEÑO
            'placeholder': 'Ej: 1',
            'min': '1',    # <-- Mínimo en Frontend (HTML)
            'max': '999'   # <-- Máximo en Frontend (HTML)
        })
    )
    numero_hasta = forms.IntegerField(
        label='Número Hasta',
        required=True,
        min_value=1,
        max_value=999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', # <-- ESTO ES CLAVE PARA EL DISEÑO
            'placeholder': 'Ej: 999',
            'min': '1',    # <-- Mínimo en Frontend (HTML)
            'max': '999'   # <-- Máximo en Frontend (HTML)
        })
    )
    
    # Validar que "desde" no sea mayor que "hasta"
    def clean(self):
        cleaned_data = super().clean()
        desde = cleaned_data.get("numero_desde")
        hasta = cleaned_data.get("numero_hasta")

        if desde and hasta and desde > hasta:
            raise forms.ValidationError("El número 'Desde' no puede ser mayor que el número 'Hasta'.")
        return cleaned_data


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