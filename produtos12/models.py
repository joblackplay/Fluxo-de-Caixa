from django.db import models
from fornecedores.models import Fornecedor


class Produto(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Produto")
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Código")
    
    preco_custo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Preço de Custo")
    preco_venda = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Preço de Venda")
    
    unidade = models.CharField(max_length=20, default="UN", choices=[
        ('UN', 'Unidade'),
        ('KG', 'Quilograma'),
        ('LT', 'Litro'),
        ('CX', 'Caixa'),
        ('PCT', 'Pacote'),
    ], verbose_name="Unidade")

    # ✅ ManyToManyField OPCIONAL (não obrigatório)
    fornecedores = models.ManyToManyField(
        'Fornecedor', 
        related_name='produtos', 
        blank=True,                    # ← Permite salvar sem fornecedor
        verbose_name="Fornecedores"
    )
    
    estoque = models.PositiveIntegerField(default=0, verbose_name="Estoque Mínimo")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def margem_lucro(self):
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0