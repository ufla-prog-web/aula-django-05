
from contas.models import Usuario
from eventos.models import Produtora, Evento
from ingressos.models import Pedido, Ingresso


def eventa_dashboard(request):
    if request.path.rstrip("/") != "/admin":
        return {}

    return {
        "total_usuarios": Usuario.objects.count(),
        "total_produtoras": Produtora.objects.count(),
        "total_eventos": Evento.objects.count(),
        "total_ingressos": Ingresso.objects.count(),
        "total_pedidos": Pedido.objects.count(),
    }
