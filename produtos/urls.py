from django.urls import path
from . import views

urlpatterns= [
   path('', views.lista_produtos, name='lista_produtos'),
   path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
   path('produtos/<int:pk>/editar/', views.editar_produto, name='editar_produto'),
   path('produtos/<int:pk>/deletar/', views.deletar_produto, name='deletar_produto'),

]