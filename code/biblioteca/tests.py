from django.test import TestCase
from .models import Livro
from .models import TCC
from django.urls import reverse

class ModeloTestCase(TestCase):
    def setUp(self):
        Livro.objects.create(nome="Introdução ao Django", autor="João Silva", ano=2024)
        TCC.objects.create(titulo="Análise de Sistemas Web", autor="José Carvalho", orientador="Prof. Carlos Souza", ano=2023)

    def test_criacao_e_conteudo_livro(self):
        livro = Livro.objects.get(nome="Introdução ao Django")
        self.assertEqual(livro.autor, "João Silva")
        self.assertEqual(livro.ano, 2024)

    def test_criacao_e_conteudo_tcc(self):
        tcc = TCC.objects.get(titulo="Análise de Sistemas Web")
        self.assertEqual(tcc.autor, "José Carvalho")
        self.assertEqual(tcc.orientador, "Prof. Carlos Souza")
        self.assertEqual(tcc.ano, 2023)

class ViewTCCTestCase(TestCase):
    def setUp(self):
        self.tcc = TCC.objects.create(titulo="Análise de Interfaces Web", autor="Cesar Silva", orientador="Prof. Ricardo Souza", ano=2022)

    def test_view_tcc_detalhes(self):
        url = reverse("tcc_detalhes", args=[self.tcc.id])
        response = self.client.get(url)
        #print(url)
        #print(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Análise de Interfaces Web")