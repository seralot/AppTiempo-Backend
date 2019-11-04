from django.test import TestCase

from api.services import getapi

# Create your tests here.

def obtener_tiempo(ubicacion):
    return []

class WeatherGetterTestCase(TestCase):
    def test_obtener_el_tiempo(self):
        respuesta = getapi("Vigo")
        self.assertEqual(40, len(respuesta))