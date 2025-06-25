from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_saida, name='cadastro_saida'),
    path('lista/', views.lista_saidas, name='lista_saidas'),
    path('editar/<int:saida_id>/', views.editar_saida, name='editar_saida'),
    path('excluir/<int:saida_id>/', views.excluir_saida, name='excluir_saida'),
    path('excluir_selecionados/', views.excluir_selecionados, name='excluir_selecionados'),
    path('salvar/', views.salvar_saidas, name='salvar_saidas'),
]
