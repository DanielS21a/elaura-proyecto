from django.test import TestCase
from django.urls import reverse

from .models import Usuario


class LoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = Usuario.objects.create_user(
            username='recepcion',
            password='clave-segura-123',
            nombre='Ana Recepción',
            rol=Usuario.Rol.RECEPCIONISTA,
        )

    def iniciar_sesion(self, url=None):
        return self.client.post(
            url or reverse('login'),
            {'username': 'recepcion', 'password': 'clave-segura-123'},
        )

    def test_url_del_login(self):
        self.assertEqual(reverse('login'), '/usuarios/login/')
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)

    def test_login_redirige_a_habitaciones(self):
        self.assertRedirects(self.iniciar_sesion(), reverse('habitaciones:lista'))

    def test_login_respeta_next(self):
        destino = reverse('habitaciones:lista') + '?orden=numero'
        respuesta = self.iniciar_sesion(f"{reverse('login')}?next={destino}")
        self.assertRedirects(respuesta, destino, fetch_redirect_response=False)

    def test_usuario_con_sesion_no_ve_el_login(self):
        self.client.force_login(self.usuario)
        self.assertRedirects(
            self.client.get(reverse('login')), reverse('habitaciones:lista')
        )

    def test_logout_vuelve_al_login(self):
        self.client.force_login(self.usuario)
        self.assertRedirects(self.client.post(reverse('logout')), reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)
