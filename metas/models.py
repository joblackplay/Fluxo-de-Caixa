from django.db import models
from django.utils import timezone

# Create your models here.
class MetaMensal(models.Model):
    mes = models.DateField(unique=True)  # Ex: 2026-04-01
    valor_meta = models.DecimalField(max_digits=12, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Meta Mensal"
        verbose_name_plural = "Metas Mensais"
        ordering = ['-mes']

    def __str__(self):
        return f"Meta de {self.mes.strftime('%m/%Y')} - R$ {self.valor_meta}"

    @staticmethod
    def get_meta_atual():
        """Retorna a meta do mês atual ou cria uma padrão"""
        hoje = timezone.now().date().replace(day=1)
        meta, created = MetaMensal.objects.get_or_create(
            mes=hoje,
            defaults={'valor_meta': 75000.00}  # Valor padrão inicial
        )
        return meta