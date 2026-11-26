from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from usuarios.models import Usuario

from . import services
from .models import Habitacion


class HabitacionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.gerente = Usuario.objects.create_user(
            'gerente', nombre='Gerente', rol=Usuario.Rol.GERENTE
        )
        cls.recepcionista = Usuario.objects.create_user(
            'recepcion', nombre='Recepción', rol=Usuario.Rol.RECEPCIONISTA
        )
        cls.url_lista = reverse('habitaciones:lista')
        cls.url_registrar = reverse('habitaciones:registrar')
        cls.datos = {'numero': 101, 'capacidad': 2, 'orientacion': 'MAR'}

    def crear(self, **cambios):
        datos = {**self.datos, 'registrada_por': self.gerente, **cambios}
        return Habitacion.objects.create(**datos)

    def test_gerente_registra_habitacion(self):
        self.client.force_login(self.gerente)
        respuesta = self.client.post(self.url_registrar, self.datos, follow=True)
        self.assertRedirects(respuesta, self.url_lista)
        self.assertContains(respuesta, 'La habitación 101 se registró correctamente.')
        habitacion = Habitacion.objects.get()
        self.assertEqual(
            (habitacion.numero, habitacion.capacidad, habitacion.orientacion),
            (101, 2, 'MAR'),
        )
        self.assertTrue(habitacion.esta_vacante())
        self.assertFalse(habitacion.eliminada)
        self.assertEqual(habitacion.registrada_por, self.gerente)

    def test_guardar_y_agregar_vuelve_al_formulario(self):
        self.client.force_login(self.gerente)
        respuesta = self.client.post(
            self.url_registrar, {**self.datos, 'guardar_y_agregar': '1'}
        )
        self.assertRedirects(respuesta, self.url_registrar)

    def test_no_acepta_campos_ajenos_al_formulario(self):
        self.client.force_login(self.gerente)
        self.client.post(
            self.url_registrar,
            {**self.datos, 'estado': 'OCUPADA', 'registrada_por': self.recepcionista.pk},
        )
        habitacion = Habitacion.objects.get()
        self.assertTrue(habitacion.esta_vacante())
        self.assertEqual(habitacion.registrada_por, self.gerente)

    def test_rechaza_datos_invalidos(self):
        self.client.force_login(self.gerente)
        casos = [
            ('numero', ''), ('numero', 0), ('numero', -1), ('numero', 'abc'),
            ('numero', 99999999999), ('capacidad', ''), ('capacidad', 0),
            ('capacidad', 40000), ('orientacion', ''), ('orientacion', 'LAGO'),
        ]
        for campo, valor in casos:
            with self.subTest(campo=campo, valor=valor):
                respuesta = self.client.post(
                    self.url_registrar, {**self.datos, campo: valor}
                )
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn(campo, respuesta.context['form'].errors)
        self.assertFalse(Habitacion.objects.exists())

    def test_rechaza_numero_duplicado(self):
        self.crear()
        self.client.force_login(self.gerente)
        respuesta = self.client.post(self.url_registrar, self.datos)
        self.assertContains(respuesta, 'Ya existe una habitación con este número.')
        self.assertEqual(Habitacion.objects.count(), 1)

    def test_permite_reutilizar_numero_de_habitacion_eliminada(self):
        self.crear(eliminada=True)
        services.registrar_habitacion(self.gerente, **self.datos)
        self.assertEqual(Habitacion.objects.filter(numero=101).count(), 2)

    def test_restricciones_de_base_de_datos(self):
        self.crear()
        for cambios in ({}, {'numero': 102, 'capacidad': 0}):
            with self.subTest(cambios), self.assertRaises(IntegrityError):
                with transaction.atomic():
                    self.crear(**cambios)

    def test_recepcionista_consulta_pero_no_registra(self):
        self.client.force_login(self.recepcionista)
        respuesta = self.client.get(self.url_lista)
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotContains(respuesta, self.url_registrar)
        self.assertEqual(self.client.get(self.url_registrar).status_code, 403)
        self.assertEqual(
            self.client.post(self.url_registrar, self.datos).status_code, 403
        )
        self.assertFalse(Habitacion.objects.exists())

    def test_sin_sesion_redirige_al_login(self):
        for url in (self.url_lista, self.url_registrar, reverse('inicio')):
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url), f'{reverse("admin:login")}?next={url}'
                )

    def test_lista_oculta_eliminadas(self):
        self.crear(numero=777, eliminada=True)
        self.crear(numero=205, estado='OCUPADA')
        self.client.force_login(self.gerente)
        respuesta = self.client.get(self.url_lista)
        self.assertEqual([h.numero for h in respuesta.context['habitaciones']], [205])
        self.assertEqual(respuesta.context['ocupadas'], 1)
        self.assertEqual(respuesta.context['vacantes'], 0)

    def test_crear_superusuario_asigna_rol_gerente(self):
        usuario = Usuario.objects.create_superuser('admin', nombre='Admin')
        self.assertTrue(usuario.es_gerente)
