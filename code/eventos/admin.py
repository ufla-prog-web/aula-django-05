from django.contrib import admin
from .models import Produtora, Evento, TipoIngresso


@admin.register(Produtora)
class ProdutoraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'email', 'telefone')
    search_fields = ('nome', 'cnpj', 'email')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'data',
        'local',
        'produtora',
        'coordenador',
        'status',
    )

    list_filter = ('status', 'data', 'produtora')
    search_fields = ('nome', 'local')


@admin.register(TipoIngresso)
class TipoIngressoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'evento', 'preco', 'quantidade')
    list_filter = ('evento',)
    search_fields = ('nome',)