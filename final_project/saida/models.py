from django.db import models
from produtos.models import Produto
from servicos.models import Servico


class Saida(models.Model):
    data_saida = models.DateTimeField(auto_now_add=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    serie = models.CharField(max_length=100, blank=True)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produto} - {self.servico} - {self.quantidade}"
