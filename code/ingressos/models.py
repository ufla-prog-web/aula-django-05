import uuid

from django.conf import settings
from django.db import models


class Pedido(models.Model):

    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        APROVADO = "APROVADO", "Aprovado"
        CANCELADO = "CANCELADO", "Cancelado"

    participante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pedidos"
    )

    data_compra = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE
    )

    def __str__(self):
        return f"Pedido #{self.id} - {self.participante.email}"


class Ingresso(models.Model):

    class Status(models.TextChoices):
        DISPONIVEL = "DISPONIVEL", "Disponível"
        UTILIZADO = "UTILIZADO", "Utilizado"
        CANCELADO = "CANCELADO", "Cancelado"

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.PROTECT,
        related_name="ingressos"
    )

    tipo_ingresso = models.ForeignKey(
        "eventos.TipoIngresso",
        on_delete=models.PROTECT,
        related_name="ingressos"
    )

    codigo = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DISPONIVEL
    )

    data_validacao = models.DateTimeField(
        null=True,
        blank=True
    )

    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ingressos_validados"
    )

    def __str__(self):
        return f"Ingresso {self.codigo}"
