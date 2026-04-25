from django.urls import path
from . import views

urlpatterns= [
    path('',views.lista_fornecedores,name='lista_fornecedores'),
    path('cadastrar',views.cadastrar_fornecedor,name='cadastrar_fornecedor'),
    path('fornecedor/<int:pk>/editar/', views.editar_fornecedor, name='editar_fornecedor'),
    path('fornecedores/<int:pk>/deletar/', views.deletar_fornecedor, name='deletar_fornecedor'),
]