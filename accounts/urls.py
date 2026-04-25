from django.urls import path
from . import views

urlpatterns= [
    path('register',views.register_view, name='register'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/<int:user_id>/get/', views.get_usuario, name='get_usuario'),
    path('usuarios/<int:user_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:user_id>/editar-role/', views.editar_role, name='editar_role'),
    path('usuarios/<int:user_id>/deletar/', views.deletar_usuario, name='deletar_usuario'),
]