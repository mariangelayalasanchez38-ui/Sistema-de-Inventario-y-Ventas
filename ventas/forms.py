from django import forms
from .models import Producto, Cliente, Proveedor


class ProductoForm(forms.ModelForm):
    precio = forms.DecimalField(
        widget=forms.TextInput,
        required=True
    )

    cantidad = forms.IntegerField(
        widget=forms.TextInput,
        required=True
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'cantidad']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo']


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'correo']