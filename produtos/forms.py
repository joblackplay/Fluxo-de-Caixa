from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome','unidade', 'preco_de_compra', 'estoque_atual', 'ativo']
