from django.db import models
from produtos.models import Produto
from servicos.models import Servico


class Entrada(models.Model):
    data_entrada = models.DateTimeField(auto_now_add=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    serie = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.produto} - {self.servico} - {self.quantidade}"
