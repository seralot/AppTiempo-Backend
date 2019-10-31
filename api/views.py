from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

import requests

# Create your views here.
def getapi(ubicacion):
    r = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?appid=375b5b72defecfdfccfa090d50f49db4&q={ubicacion}&units=metric&lang=es')
    return r.text


class MyView(View):

    def get(self, request, *args, **kwargs):
        print(request.GET)
        city = request.GET['city']
        r=getapi(city)
        return HttpResponse(r)
