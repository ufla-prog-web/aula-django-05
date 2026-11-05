from django.test import Client, TestCase
from django.urls import reverse

from .models import Usuario


class AdminLoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Usuario.objects.create_superuser(
            email="admin@example.com", password="test-password-123"
        )

    def test_login_with_csrf_redirects_to_dashboard(self):
        client = Client(enforce_csrf_checks=True)
        response = client.get(reverse("admin:login"))
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="next" value="/admin/"')
        response = client.post(reverse("admin:login"), {
            "username": "admin@example.com",
            "password": "test-password-123",
            "next": reverse("admin:index"),
            "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        })
        self.assertRedirects(response, reverse("admin:index"))

    def test_invalid_password_displays_error(self):
        response = self.client.post(reverse("admin:login"), {
            "username": "admin@example.com",
            "password": "wrong-password",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertContains(response, 'class="errorlist nonfield"')
        self.assertContains(response, 'value="admin@example.com"')

    def test_jazzmin_and_theme_assets_on_admin_pages(self):
        self.client.force_login(Usuario.objects.get(email="admin@example.com"))
        for url in (
            reverse("admin:index"),
            reverse("admin:eventos_evento_changelist"),
            reverse("admin:eventos_evento_add"),
            reverse("admin:password_change"),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, 'id="jazzy-navbar"')
                self.assertContains(response, 'id="jazzmin-dark-mode-theme"')
                self.assertContains(response, 'js/admin.js', count=1)

    def test_login_uses_jazzmin_registration_base(self):
        response = self.client.get(reverse("admin:login"))
        self.assertContains(response, 'jazzmin-login-page')
        self.assertContains(response, 'id="jazzmin-dark-mode-theme"')
        self.assertContains(response, 'js/admin.js', count=1)
