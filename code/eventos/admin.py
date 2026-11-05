from django.contrib import admin

from .models import Produtora, Evento, TipoIngresso
from .filters import PeriodoEventoFilter, PrecoIngressoFilter, ProdutoraComEventosFilter


@admin.register(Produtora)
class ProdutoraAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "email", "telefone")
    search_fields = ("nome", "cnpj", "email")
    list_filter = (ProdutoraComEventosFilter, "data_cadastro")
    date_hierarchy = "data_cadastro"


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "data",
        "horario",
        "produtora",
        "coordenador",
        "status",
    )

    list_filter = (
        "status", PeriodoEventoFilter, "data",
        ("produtora", admin.RelatedOnlyFieldListFilter),
        ("coordenador", admin.RelatedOnlyFieldListFilter),
    )
    date_hierarchy = "data"
    list_select_related = ("produtora", "coordenador")
    search_fields = ("nome", "local")
    filter_horizontal = ("organizadores",)


@admin.register(TipoIngresso)
class TipoIngressoAdmin(admin.ModelAdmin):
    list_display = ("nome", "evento", "preco", "quantidade")
    list_filter = (
        ("evento", admin.RelatedOnlyFieldListFilter),
        ("evento__produtora", admin.RelatedOnlyFieldListFilter),
        PrecoIngressoFilter,
    )
    list_select_related = ("evento",)
    search_fields = ("nome", "evento__nome")
