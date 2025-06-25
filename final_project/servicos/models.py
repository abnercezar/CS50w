from django.db import models


class Servico(models.Model):
    servico = models.CharField(max_length=200)
    observacoes = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.servico
