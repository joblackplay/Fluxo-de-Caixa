from django.urls import path
from . import views

urlpatterns = [
    
    # Entradas
    path('entradas/', views.entradas_list, name='entradas_list'),
    path('entrada/create/', views.entrada_create, name='entrada_create'),
    
    # Saídas
    path('saidas/', views.saidas_list, name='saidas_list'),
    path('saida/create/', views.saida_create, name='saida_create'),
    
    # Tipos
    path('tipos/entrada/', views.tipos_entrada, name='tipos_entrada'),
    path('tipos/saida/', views.tipos_saida, name='tipos_saida'),
]