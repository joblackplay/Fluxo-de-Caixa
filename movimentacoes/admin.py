from django.contrib import admin
from .models import TipoEntrada,TipoSaida,Entrada,Saida

# Register your models here.



class TipoEntradaAdmin(admin.ModelAdmin):
    list_display = ['nome','descricao']
    ordering = ['descricao']


class TipoSaidaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    ordering = ['descricao']


class SaidaAdmin(admin.ModelAdmin):
    list_display = ['tipo','valor', 'descricao','pagamento']
    list_filter = ['tipo','data']
    

class EntradaAdmin(admin.ModelAdmin):
    list_display = ['tipo','valor', 'descricao','pagamento']
    list_filter = ['tipo','data']


admin.site.register(TipoEntrada,TipoEntradaAdmin)
admin.site.register(TipoSaida,TipoSaidaAdmin)
admin.site.register(Entrada,EntradaAdmin)
admin.site.register(Saida,SaidaAdmin)
