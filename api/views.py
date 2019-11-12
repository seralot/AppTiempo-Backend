import datetime as dt
import pendulum 

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

import json

import requests

from api.services import getapi
from api.handler import Handler
from db import models

# Create your views here.

class MyView(View):
    def get(self, request, *args, **kwargs):
        city = request.GET['city']
        day = self._sanitize_day(request.GET.get('day', None))


        r=getapi(city)
        data = json.loads(r)
        # fechaAPI = data["list"][0]["dt_txt"].split()
        

        # TODO: convertir el date de string a clase python    
        handler = Handler(data)
        handler.main()
        handler.check_db(city.capitalize(), day)

        
        return HttpResponse(r)


    def _sanitize_day(self, day = None):
        if day is None:
            return dt.date.today()

        try:
            return pendulum.from_format(day, "YYYY-MM-DD")
        except:
            return dt.date.today()


    # def _checkDB(self, city: models.City, day: Date):
    #     if models.City.objects.filter(name=city).exists():
    #         cityDB = models.City.objects.get(name=city)
    #         if models.Day.objects.filter(date = day, city = cityDB).exists():
    #             result = models.Day.objects.get(date = day, city = cityDB)
    #             return True
    #             print(">>>>>>>>>>>>>>>>>>>>>>>>> Existe", result)
    #         else:
    #             return False
    #             print(">>>>>>>>>>>>>>>>>>>>>>>> No existe", fecha," en ", cityDB)
    #     else:
    #         print(">>>>>>>>>>>>>>>>>>>>>>>>>>> No existe", city)
    #         return 
            