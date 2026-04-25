from django import forms
from .models import Fornecedor

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'cpf', 'telefone', 'email', 'endereco', 'cidade', 'estado', 'observacoes', 'ativo']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }