import json

from django.test import TestCase, Client
from backend.models import Officer

class CargarInfraccionTestCase(TestCase):
    fixtures = ["officer.json", "person.json", "vehicle.json"]

    def setUp(self):
        self.client = Client()
        self.path = "/cargar_infraccion/"

    def test_put_method(self):
        """ Caso de prueba que verifica si
            métodos como PUT no se permiten.
            Este método sólo permite solicitudes POST
        """

        response = self.client.put(path=self.path)
        # Devuelve 405: METHOD NOT ALLOWED
        self.assertEqual(405, response.status_code)

    def test_unvalid_token(self):
        """ Caso de prueba que verifica que tokens
            mal compuestas o no válidas sean rechazadas
        """
        # hacer POST con token mal compuesta
        response = self.client.post(path=self.path,
            HTTP_AUTHORIZATION="TOKEN_INVALIDA")
        self.assertEqual(403, response.status_code)

        # hacer POST con token que no existe
        response = self.client.post(path=self.path,
            HTTP_AUTHORIZATION="Bearer TOKEN_INVALIDA")
        self.assertEqual(403, response.status_code)

    def test_non_existent_vehicle(self):
        """ Caso de prueba que intentan publicar
            una infracción a un vehículo que no existe.
        """

        data = {
            "placa_patente": "PLACA_NO_EXISTENTE",
            "comentarios": "Comentarios del oficial"
        }
        officer = Officer.objects.get(pk=1)
        # Hacer POST con placa que no existe
        response = self.client.post(path=self.path,
            data=json.dumps(data), content_type="json",
            HTTP_AUTHORIZATION=f"Bearer { officer.token }")
        self.assertEqual(404, response.status_code)

    def test_valid_post(self):
        """ Caso de prueba válido que publica una
            infracción asociada al oficial, vehículo y persona
            que se cargan en los fixtures.
        """
        data = {
            "placa_patente": "GPZ402",
            "comentarios": "Comentarios del oficial"
        }
        officer = Officer.objects.get(pk=1)
        response = self.client.post(path=self.path,
            data=json.dumps(data), content_type="json",
            HTTP_AUTHORIZATION=f"Bearer { officer.token }")
        self.assertEqual(200, response.status_code)

class GenerarInformeTestCase(TestCase):
    fixtures = ["officer.json", "person.json", "vehicle.json",
        "infractions.json"]

    def setUp(self):
        self.client = Client()
        self.path = "/generar_informe/"

    def test_non_existent_person(self):
        """ Caso de prueba con email de persona
            que no existe.
        """
        response = self.client.get(path=self.path, data={"email": "NO_EXISTE"})
        self.assertEqual(404, response.status_code)

    def test_non_existent_person(self):
        """ Caso de prueba exitoso que retorna
            un objeto JSON con las infracciones de la
            persona requerida.
        """
        # Validar si la respuesta es exitosa
        response = self.client.get(path=self.path, data={"email": "pedro@gmail.com"})
        self.assertEqual(200, response.status_code)

        # Validar si el cuerpo de la respuesta es una lista
        response_data = json.loads(response.content)
        self.assertIsInstance(response_data, list)

        # Validar si tiene las llaves cada objeto
        expected_keys = {"id", "vehicle_id", "comments", "officer_id",
            "created_at"}
        for infraction in response_data:
            self.assertSetEqual(expected_keys, set(infraction.keys()))