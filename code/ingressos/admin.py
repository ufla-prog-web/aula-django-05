from django.contrib import admin
from .models import Pedido, Ingresso


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'participante',
        'data_compra',
        'valor_total',
        'status',
    )

    list_filter = ('status', 'data_compra')
    search_fields = ('participante__email',)


@admin.register(Ingresso)
class IngressoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'pedido',
        'tipo_ingresso',
        'status',
        'data_validacao',
        'organizador',
    )

    list_filter = ('status',)
    search_fields = ('codigo',)