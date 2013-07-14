from django.db import models


class Enquete(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)


class Opcao(models.Model):
    titulo = models.CharField(max_length=100)
    enquete = models.ForeignKey(Enquete)


class Voto(models.Model):
    opcao = models.ForeignKey(Opcao)
    data = models.DateTimeField(auto_now_add=True)
