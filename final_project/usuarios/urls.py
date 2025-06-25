from django.urls import path
from . import views

# Lista de URLs da aplicação 'usuarios'
urlpatterns = [
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
]
