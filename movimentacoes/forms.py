from django import forms
from .models import Entrada, Saida, TipoEntrada, TipoSaida

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ['tipo', 'descricao', 'valor', 'pagamento', 'observacao']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição da entrada'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class SaidaForm(forms.ModelForm):
    class Meta:
        model = Saida
        fields = ['tipo', 'descricao', 'valor', 'pagamento', 'observacao']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class TipoEntradaForm(forms.ModelForm):
    class Meta:
        model = TipoEntrada
        fields = ['nome', 'descricao']

class TipoSaidaForm(forms.ModelForm):
    class Meta:
        model = TipoSaida
        fields = ['nome', 'descricao']