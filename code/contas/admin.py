from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    model = Usuario

    list_display = (
        'email',
        'first_name',
        'last_name',
        'perfil',
        'produtora',
        'is_active',
        'is_staff',
    )

    list_filter = (
        'perfil',
        'is_active',
        'is_staff',
    )

    search_fields = (
        'email',
        'first_name',
        'last_name',
    )

    ordering = ('email',)

    fieldsets = (
        ('Informações pessoais', {
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password',
            )
        }),
        ('Perfil e produtora', {
            'fields': (
                'perfil',
                'produtora',
            )
        }),
        ('Permissões', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Datas importantes', {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'perfil',
                'produtora',
                'password1',
                'password2',
            ),
        }),
    )