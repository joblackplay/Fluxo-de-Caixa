from django.urls import path
from . import views

urlpatterns = [
    
    # Entradas
    path('entradas/', views.entradas_list, name='entradas_list'),
    path('entradas/create/', views.entrada_create, name='entrada_create'),
    path('entrada/<int:pk>/edit/', views.entrada_edit, name='entrada_edit'),
    path('entrada/<int:pk>/delete/', views.entrada_delete, name='entrada_delete'),
    
    # Saídas
    path('saidas/', views.saidas_list, name='saidas_list'),
    path('saida/create/', views.saida_create, name='saida_create'),
    path('saida/<int:pk>/delete/', views.saida_delete, name='saida_delete'),
    path('saida/<int:pk>/edit/', views.saida_edit, name='saida_edit'),

    path('dre/', views.dre, name='dre'),
    path('fluxo-de-caixa/', views.fluxo_de_caixa, name='fluxo_de_caixa'),

    path('relatorios/produtos-fornecedor/', views.relatorio_produtos_fornecedor, name='relatorio_produtos_fornecedor'),
    path('relatorios/por-tipo-saida/', views.relatorio_por_tipo_saida, name='relatorio_por_tipo_saida'),
    path('relatorios/geral-por-tipo/', views.relatorio_geral_por_tipo, name='relatorio_geral_por_tipo'),
    path('relatorios/por-tipo-movimentacao/', views.relatorio_por_tipo_movimentacao, name='relatorio_por_tipo_movimentacao'),
    
]