from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro_produto, name='cadastro_produto'),
    path('', views.lista_produtos, name='lista_produtos'),
    path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
    path('<int:produto_id>/valor/', views.obter_valor_produto, name='obter_valor_produto'),
]
