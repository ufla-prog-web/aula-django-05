from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    ordering = ("email",)

    list_display = (
        "email",
        "first_name",
        "last_name",
        "perfil",
        "produtora",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "perfil",
        "is_active",
        "is_staff",
        ("produtora", admin.RelatedOnlyFieldListFilter),
        "date_joined",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    readonly_fields = ("last_login", "date_joined")
    list_select_related = ("produtora",)

    fieldsets = (
        ("Acesso", {
            "fields": ("email", "password")
        }),
        ("Informações pessoais", {
            "fields": ("first_name", "last_name")
        }),
        ("Perfil do sistema", {
            "fields": ("perfil", "produtora")
        }),
        ("Permissões", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Datas", {
            "fields": ("last_login", "date_joined")
        }),
    )

    add_fieldsets = (
        ("Novo usuário", {
            "classes": ("wide",),
            "fields": (
                "email",
                "perfil",
                "password1",
                "password2",
            ),
        }),
    )
