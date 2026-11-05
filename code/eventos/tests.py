from datetime import time, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from contas.models import Usuario
from ingressos.models import Ingresso, Pedido
from .models import Evento, Produtora, TipoIngresso


class AdminFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.produtora = Produtora.objects.create(nome="Produtora A", cnpj="111", email="a@example.com")
        cls.vazia = Produtora.objects.create(nome="Produtora B", cnpj="222", email="b@example.com")
        cls.admin = Usuario.objects.create_superuser(email="admin@example.com", password="test-password")
        cls.coordenador = Usuario.objects.create_user(
            email="coord@example.com", perfil="COORDENADOR", produtora=cls.produtora,
        )
        cls.eventos = {}
        for dias in (-1, 0, 6, 7):
            cls.eventos[dias] = Evento.objects.create(
                nome=f"Evento {dias}", data=timezone.localdate() + timedelta(days=dias),
                horario=time(18), local="Teatro", capacidade=100,
                produtora=cls.produtora, coordenador=cls.coordenador,
                status="PUBLICADO" if dias == 0 else "RASCUNHO",
            )
        cls.gratuito = TipoIngresso.objects.create(nome="Cortesia", preco=0, quantidade=10, evento=cls.eventos[0])
        cls.pago = TipoIngresso.objects.create(nome="Inteira", preco=50, quantidade=90, evento=cls.eventos[7])
        cls.pedido = Pedido.objects.create(participante=cls.coordenador, valor_total=0)
        cls.outro_pedido = Pedido.objects.create(participante=cls.admin, valor_total=50)
        for _ in range(2):
            Ingresso.objects.create(pedido=cls.pedido, tipo_ingresso=cls.gratuito)
        cls.utilizado = Ingresso.objects.create(
            pedido=cls.outro_pedido, tipo_ingresso=cls.pago, status="UTILIZADO",
            organizador=cls.coordenador, data_validacao=timezone.now(),
        )

    def setUp(self):
        self.client.force_login(self.admin)

    def results(self, model, params):
        response = self.client.get(reverse(f"admin:{model}_changelist"), params)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "jazzmin")
        return list(response.context["cl"].queryset.values_list("pk", flat=True))

    def test_event_period_boundaries(self):
        for value, days in (("hoje", [0]), ("proximos_7", [0, 6]), ("futuros", [6, 7]), ("passados", [-1])):
            with self.subTest(value=value):
                self.assertCountEqual(self.results("eventos_evento", {"periodo": value}),
                                      [self.eventos[day].pk for day in days])

    def test_combined_filters_and_search(self):
        params = {"periodo": "proximos_7", "status__exact": "PUBLICADO",
                  "produtora__id__exact": self.produtora.pk, "q": "Evento"}
        self.assertEqual(self.results("eventos_evento", params), [self.eventos[0].pk])
        params["status__exact"] = "CANCELADO"
        self.assertEqual(self.results("eventos_evento", params), [])

    def test_producers_with_and_without_events_have_no_duplicates(self):
        self.assertEqual(self.results("eventos_produtora", {"com_eventos": "sim"}), [self.produtora.pk])
        self.assertEqual(self.results("eventos_produtora", {"com_eventos": "nao"}), [self.vazia.pk])

    def test_free_and_paid_ticket_types(self):
        self.assertEqual(self.results("eventos_tipoingresso", {"preco_tipo": "gratuito"}), [self.gratuito.pk])
        self.assertEqual(self.results("eventos_tipoingresso", {"preco_tipo": "pago"}), [self.pago.pk])

    def test_orders_filtered_by_event_are_not_duplicated(self):
        params = {"ingressos__tipo_ingresso__evento__id__exact": self.eventos[0].pk}
        self.assertEqual(self.results("ingressos_pedido", params), [self.pedido.pk])

    def test_tickets_by_event_producer_and_validator(self):
        params = {"tipo_ingresso__evento__id__exact": self.eventos[7].pk,
                  "tipo_ingresso__evento__produtora__id__exact": self.produtora.pk,
                  "organizador__id__exact": self.coordenador.pk, "status__exact": "UTILIZADO"}
        self.assertEqual(self.results("ingressos_ingresso", params), [self.utilizado.pk])

    def test_users_by_producer_and_profile(self):
        params = {"produtora__id__exact": self.produtora.pk, "perfil__exact": "COORDENADOR"}
        self.assertEqual(self.results("contas_usuario", params), [self.coordenador.pk])

    def test_unknown_custom_filter_does_not_hide_results(self):
        self.assertEqual(len(self.results("eventos_evento", {"periodo": "invalido"})), 4)
