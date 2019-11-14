import datetime as dt
import pendulum 

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.utils.timezone import now


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

        
        handler = Handler()
        
        if(handler.check_db(city.capitalize(), day)):
            modelCity = models.City.objects.get(name = city.capitalize())
            modelDay = models.Day.objects.get(date=day, city=modelCity)
            
            if((modelDay.update_at.hour - now().hour)<=2):
                records = handler.get_weather_records(city.capitalize(), day)
                self._update_day(day, modelCity)
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

    def _update_day(self, fecha, city):
        dayupdate, created = models.Day.objects.update_or_create(
            date=fecha,
            city=city,
            defaults={'update_at': now()}
        )