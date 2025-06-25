from django import forms
from .models import Saida


class SaidaForm(forms.ModelForm):

    class Meta:
        model = Saida
        fields = ['produto', 'servico', 'quantidade', 'valor_unitario']
        widgets = {
            'valor_unitario': forms.HiddenInput()
        }
