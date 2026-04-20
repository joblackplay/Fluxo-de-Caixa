from django.urls import path
from . import views

urlpatterns = [
    path('salvar/', views.salvar_meta_mensal, name='salvar_meta_mensal'),
    path('historico/', views.historico_metas, name='historico_metas'),
]
    