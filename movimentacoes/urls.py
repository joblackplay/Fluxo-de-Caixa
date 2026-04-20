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
    
]