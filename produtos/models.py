from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Produto")
    unidade = models.CharField(max_length=20, default="UN", choices=[
        ('UN', 'Unidade'),
        ('KG', 'Quilograma'),
        ('LT', 'Litro'),
        ('CX', 'Caixa'),
        ('PCT', 'Pacote'),
    ], verbose_name="Unidade")
    preco_de_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Preço de Compra")
    estoque_atual = models.FloatField(default=0, verbose_name="Estoque Atual")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return self.nome