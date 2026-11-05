from django.conf import settings
from django.db import models


class Produtora(models.Model):
    nome = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, unique=True)
    descricao = models.TextField(blank=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Evento(models.Model):

    class Status(models.TextChoices):
        RASCUNHO = "RASCUNHO", "Rascunho"
        PUBLICADO = "PUBLICADO", "Publicado"
        ENCERRADO = "ENCERRADO", "Encerrado"
        CANCELADO = "CANCELADO", "Cancelado"

    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    data = models.DateField()
    horario = models.TimeField()
    local = models.CharField(max_length=200)
    capacidade = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RASCUNHO
    )

    produtora = models.ForeignKey(
        Produtora,
        on_delete=models.PROTECT,
        related_name="eventos"
    )

    coordenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="eventos_criados"
    )

    organizadores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="eventos_alocados"
    )

    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class TipoIngresso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()

    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name="tipos_ingresso"
    )

    def __str__(self):
        return f"{self.nome} - {self.evento.nome}"
