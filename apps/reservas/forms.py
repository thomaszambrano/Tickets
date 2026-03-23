# Autor: Thomas Osorio

from django import forms
from .models import Reserva
from apps.eventos.models import TipoTicket


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['tipo_ticket', 'cantidad']

    def __init__(self, *args, evento=None, **kwargs):
        super().__init__(*args, **kwargs)
        if evento:
            # Limitar los tipos de ticket solo al evento solicitado (DRY: filtro centralizado)
            self.fields['tipo_ticket'].queryset = TipoTicket.objects.filter(
                evento=evento, cantidad_disponible__gt=0
            )

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        tipo_ticket = self.cleaned_data.get('tipo_ticket')
        if tipo_ticket and cantidad and cantidad > tipo_ticket.cantidad_disponible:
            raise forms.ValidationError(
                f'Solo hay {tipo_ticket.cantidad_disponible} tickets disponibles.'
            )
        return cantidad
