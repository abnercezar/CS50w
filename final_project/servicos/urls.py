from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_servico, name='cadastro_servico'),
    path('lista/', views.lista_servicos, name='lista_servicos'),
    path('editar/<int:servico_id>/', views.editar_servico, name='editar_servico'),
    path('excluir/<int:servico_id>/', views.excluir_servico, name='excluir_servico'),
    path('<int:servico_id>/valor/', views.obter_valor_servico, name='obter_valor_servico'),
]
