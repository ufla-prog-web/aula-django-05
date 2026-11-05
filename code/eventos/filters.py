from datetime import timedelta

from django.contrib import admin
from django.db.models import Exists, OuterRef
from django.utils import timezone

from .models import Evento


class PeriodoEventoFilter(admin.SimpleListFilter):
    title = "período do evento"
    parameter_name = "periodo"

    def lookups(self, request, model_admin):
        return (
            ("hoje", "Hoje"),
            ("proximos_7", "Próximos 7 dias (inclui hoje)"),
            ("futuros", "Após hoje"),
            ("passados", "Antes de hoje"),
        )

    def queryset(self, request, queryset):
        hoje = timezone.localdate()
        if self.value() == "hoje":
            return queryset.filter(data=hoje)
        if self.value() == "proximos_7":
            return queryset.filter(data__range=(hoje, hoje + timedelta(days=6)))
        if self.value() == "futuros":
            return queryset.filter(data__gt=hoje)
        if self.value() == "passados":
            return queryset.filter(data__lt=hoje)
        return queryset


class ProdutoraComEventosFilter(admin.SimpleListFilter):
    title = "eventos cadastrados"
    parameter_name = "com_eventos"

    def lookups(self, request, model_admin):
        return (("sim", "Com eventos"), ("nao", "Sem eventos"))

    def queryset(self, request, queryset):
        if self.value() in {"sim", "nao"}:
            eventos = Evento.objects.filter(produtora_id=OuterRef("pk"))
            return queryset.alias(tem_eventos=Exists(eventos)).filter(
                tem_eventos=self.value() == "sim"
            )
        return queryset


class PrecoIngressoFilter(admin.SimpleListFilter):
    title = "preço do ingresso"
    parameter_name = "preco_tipo"

    def lookups(self, request, model_admin):
        return (("gratuito", "Gratuito"), ("pago", "Pago"))

    def queryset(self, request, queryset):
        if self.value() == "gratuito":
            return queryset.filter(preco=0)
        if self.value() == "pago":
            return queryset.filter(preco__gt=0)
        return queryset
