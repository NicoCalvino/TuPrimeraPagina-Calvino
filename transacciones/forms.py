from django import forms
from transacciones.models import *
from decimal import Decimal

class TransaccionCompraForm(forms.ModelForm):
    numero_tarjeta = forms.CharField(
        label="Número de Tarjeta",
        max_length=19,
        required=True, # Obligatorio
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: XXXX-XXXX-XXXX-XXXX',
            'pattern': '[0-9-]*',
            'title': 'Solo números y guiones'
        })
    )

    class Meta:
        model = Transaccion
        fields = ["monto", "detalle"]
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1500.50', 'min': '0'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ej: Pago de mercadería a proveedor X', 'rows': '3'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        monto = cleaned_data.get('monto')
        numero_tarjeta = cleaned_data.get('numero_tarjeta')
        
        if not numero_tarjeta:
            self.add_error('numero_tarjeta', "El número de tarjeta es obligatorio para realizar una compra.")
            return cleaned_data
        
        if not monto:
            return cleaned_data
        
        try:
            tarjeta_obj = Tarjeta.objects.get(codigo=numero_tarjeta)
        except Tarjeta.DoesNotExist:
            self.add_error('numero_tarjeta', "El número de tarjeta ingresado no existe.")
        
        monto_decimal = Decimal(str(monto))

        nuevo_saldo = tarjeta_obj.saldo - monto_decimal

        if nuevo_saldo < Decimal('-2000'):
            self.add_error('numero_tarjeta', "Saldo insuficiente")

        cleaned_data['tarjeta_objeto'] = tarjeta_obj
        cleaned_data['nuevo_saldo_tarjeta'] = nuevo_saldo

        return cleaned_data
    
class TransaccionCargaForm(forms.ModelForm):
    numero_tarjeta = forms.CharField(
        label="Número de Tarjeta",
        max_length=19,
        required=True, # Obligatorio
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: XXXX-XXXX-XXXX-XXXX',
            'pattern': '[0-9-]*',
            'title': 'Solo números y guiones'
        })
    )

    class Meta:
        model = Transaccion
        fields = ["monto"]
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1500.50', 'min': '0'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        monto = cleaned_data.get('monto')
        numero_tarjeta = cleaned_data.get('numero_tarjeta')
        
        if not numero_tarjeta:
            self.add_error('numero_tarjeta', "El número de tarjeta es obligatorio para realizar una carga.")
            return cleaned_data
        
        if not monto:
            return cleaned_data
        
        try:
            tarjeta_obj = Tarjeta.objects.get(codigo=numero_tarjeta)
        except Tarjeta.DoesNotExist:
            self.add_error('numero_tarjeta', "El número de tarjeta ingresado no existe.")
        
        monto_decimal = Decimal(str(monto))

        nuevo_saldo = tarjeta_obj.saldo + monto_decimal

        cleaned_data['tarjeta_objeto'] = tarjeta_obj
        cleaned_data['nuevo_saldo_tarjeta'] = nuevo_saldo

        return cleaned_data