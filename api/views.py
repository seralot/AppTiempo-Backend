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


        
        # fechaAPI = data["list"][0]["dt_txt"].split()
        

        # TODO: convertir el date de string a clase python    
        
        handler = Handler()
        
        if(handler.check_db(city.capitalize(), day)):
             records = handler.get_weather_records(city.capitalize(), day)
             return HttpResponse(json.dumps(records))
        else:
            r=getapi(city)
            data = json.loads(r)
            handler.main(data)
            records = handler.get_weather_records(city.capitalize(), day)
            print("SDFSKLMSDFKJDFJKFGHJVGFGFHGFKJGFBKJO API")
            return HttpResponse(json.dumps(records))
            
            
        


    def _sanitize_day(self, day = None):
        if day is None:
            return dt.date.today()

        try:
            return pendulum.from_format(day, "YYYY-MM-DD")
        except:
            return dt.date.today()
