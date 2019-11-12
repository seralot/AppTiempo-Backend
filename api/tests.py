import datetime as dt 
import json
import pendulum
from django.test import TestCase

from api.services import getapi
from api.handler import Handler
from api.views import MyView
from db import models

# Create your tests here.

def obtener_tiempo(ubicacion):
    return []


# class WeatherGetterTestCase(TestCase):
#     def test_obtener_el_tiempo(self):
#         respuesta = getapi("Vigo")
#         self.assertEqual(40, len(respuesta))

class CheckDatabaseTestCase(TestCase):
    def data(self, city):
        r=getapi(city)
        data = json.loads(r)
        fecha = data["list"][16]["dt_txt"].split()
        handler = Handler(data)
        handler.main()

        return handler, fecha

    def test_exist_database(self):
        handler, fecha = self.data('vigo')
        date = pendulum.from_format(fecha[0], "YYYY-MM-DD")
        # fecha = dt.datetime(2019,11,11,00,00,00)
        string = 'vigo'
        city = string.capitalize()
        result = handler.check_db(city, date)
        self.assertTrue(result)

    def test_city_notexists_database(self):
        handler, fecha = self.data('Sevilla')
        fecha = pendulum.from_format(fecha[0], "YYYY-MM-DD")
        result = handler.check_db('Sevilla', fecha)
        self.assertFalse(result)
    
    def test_date_notexists_database(self):
        handler, _ = self.data('Vigo')
        fecha = pendulum.from_format('2019-11-25', "YYYY-MM-DD")
        result = handler.check_db('Vigo', fecha)
        self.assertFalse(result)



    
class TestMyView(TestCase):
    def test_my_view(self):
        response = self.client.get("/api/data/", {'city': 'vigo'})

        assert 200 == response.status_code
        data = json.loads(response.content)
        assert "Vigo" == data["city"]
        