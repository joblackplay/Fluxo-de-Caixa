from django.db import models
from django.utils import timezone

class TipoEntrada(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de Entrada"
        verbose_name_plural = "Tipos de Entrada"
        ordering = ['nome']


class TipoSaida(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de Saída"
        verbose_name_plural = "Tipos de Saída"
        ordering = ['nome']


class Entrada(models.Model):
    tipo = models.ForeignKey(TipoEntrada, on_delete=models.PROTECT, related_name='entradas')
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    pagamento = models.CharField(max_length=30,default="Vendas")
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Entrada - {self.descricao[:50]}"

    class Meta:
        ordering = ['-data', '-hora']
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"


class Saida(models.Model):
    tipo = models.ForeignKey(TipoSaida, on_delete=models.PROTECT, related_name='saidas')
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    pagamento = models.CharField(max_length=30)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Saída - {self.descricao[:50]}"

    class Meta:
        ordering = ['-data', '-hora']
        verbose_name = "Saída"
        verbose_name_plural = "Saídas"