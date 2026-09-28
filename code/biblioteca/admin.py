from django.contrib import admin
from .models import Livro
from .models import TCC

class LivroAdmin(admin.ModelAdmin):
    list_display = ("nome", "autor", "ano")
    search_fields = ("nome", "autor")
    list_filter = ("autor", "ano")

class TCCAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "orientador", "ano")
    search_fields = ("titulo", "autor", "orientador")
    list_filter = ("autor", "orientador", "ano")
    ordering = ('autor',)
    list_editable = ('ano',) 

admin.site.register(Livro, LivroAdmin)
admin.site.register(TCC, TCCAdmin)

admin.site.site_header = "Administração da Biblioteca"
admin.site.index_title = "Bem-vindo a Administração do Portal Biblioteca"