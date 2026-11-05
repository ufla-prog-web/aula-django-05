
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from contas.models import Usuario
from eventos.models import Produtora, Evento
from ingressos.models import Pedido, Ingresso


@staff_member_required
def dashboard(request):
    contexto = {
        "total_produtoras": Produtora.objects.count(),
        "total_eventos": Evento.objects.count(),
        "total_ingressos": Ingresso.objects.count(),
        "total_pedidos": Pedido.objects.count(),
        "total_usuarios": Usuario.objects.count(),
    }

    return render(request, "painel/dashboard.html", contexto)
