from django import forms
from .models import Producto


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
        