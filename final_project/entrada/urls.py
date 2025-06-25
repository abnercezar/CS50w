from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_entrada, name='cadastro_entrada'),
    path('lista/', views.lista_entradas, name='lista_entradas'),
    path('editar/<int:entrada_id>/', views.editar_entrada, name='editar_entrada'),
    path('excluir/<int:entrada_id>/', views.excluir_entrada, name='excluir_entrada'),
    path('salvar/', views.salvar_entradas, name='salvar_entradas'),
    path('excluir_selecionados/', views.excluir_selecionados, name='excluir_selecionados'),
]
