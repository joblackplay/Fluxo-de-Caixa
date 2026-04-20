from django.urls import path
from . import views

urlpatterns = [
    
    # Entradas
    path('entradas/', views.entradas_list, name='entradas_list'),
    path('entradas/create/', views.entrada_create, name='entrada_create'),
    path('entrada/<int:pk>/edit/', views.entrada_edit, name='entrada_edit'),
    # path('entrada/<int:pk>/get/', views.entrada_get, name='entrada_get'),
    path('entrada/<int:pk>/delete/', views.entrada_delete, name='entrada_delete'),
    
    # Saídas
    path('saidas/', views.saidas_list, name='saidas_list'),
    path('saida/create/', views.saida_create, name='saida_create'),
    path('saida/<int:pk>/delete/', views.saida_delete, name='saida_delete'),
    path('saida/<int:pk>/edit/', views.saida_edit, name='saida_edit'),


    
    # Tipos
    # path('tipos/entrada/', views.tipos_entrada, name='tipos_entrada'),
    # path('tipos/saida/', views.tipos_saida, name='tipos_saida'),
]