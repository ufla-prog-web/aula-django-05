
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório.")

        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("perfil", "ADMINISTRADOR")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário precisa ter is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário precisa ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):

    class Perfil(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        VENDEDOR = "VENDEDOR", "Vendedor"
        COORDENADOR = "COORDENADOR", "Coordenador"
        ORGANIZADOR = "ORGANIZADOR", "Organizador"
        PARTICIPANTE = "PARTICIPANTE", "Participante"

    username = None

    email = models.EmailField(unique=True)

    perfil = models.CharField(
        max_length=20,
        choices=Perfil.choices
    )

    produtora = models.ForeignKey(
        "eventos.Produtora",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coordenadores"
    )

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["perfil"]

    def __str__(self):
        return f"{self.get_full_name() or self.email} - {self.get_perfil_display()}"

