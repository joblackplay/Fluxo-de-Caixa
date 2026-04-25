from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'codigo', 'descricao', 'preco_custo', 'preco_venda', 
                  'unidade', 'fornecedores', 'estoque_minimo', 'ativo']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'fornecedores': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
    
    # Torna o campo fornecedores opcional no formulário
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fornecedores'].required = False