from django.contrib import admin

from .models import Pedido, Ingresso


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "participante",
        "data_compra",
        "valor_total",
        "status",
    )

    list_filter = (
        "status", "data_compra",
        ("ingressos__tipo_ingresso__evento", admin.RelatedOnlyFieldListFilter),
    )
    date_hierarchy = "data_compra"
    list_select_related = ("participante",)
    search_fields = ("participante__email",)


@admin.register(Ingresso)
class IngressoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "pedido",
        "tipo_ingresso",
        "status",
        "data_validacao",
        "organizador",
    )

    list_filter = (
        "status", "data_validacao",
        ("tipo_ingresso__evento", admin.RelatedOnlyFieldListFilter),
        ("tipo_ingresso__evento__produtora", admin.RelatedOnlyFieldListFilter),
        ("organizador", admin.RelatedOnlyFieldListFilter),
    )
    date_hierarchy = "data_validacao"
    list_select_related = ("pedido__participante", "tipo_ingresso__evento", "organizador")
    search_fields = ("codigo", "pedido__participante__email")
    readonly_fields = ("codigo",)
