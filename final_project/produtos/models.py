from django.db import models


class Produto(models.Model):
    produto = models.CharField(max_length=100)
    versao = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.produto} - {self.versao}"
