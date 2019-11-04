from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

import json

import requests

from api.services import getapi
from db import models

# Create your views here.

class MyView(View):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        city = request.GET['city']
        r=getapi(city)
        data = json.loads(r)
        # comprobar si exite la ciudad en la DB, sino existe se crea
        qs = models.City.objects.filter(name=data["city"]["name"])
        if not len(qs):
            models.City.objects.create(name=data["city"]["name"])
        return HttpResponse(r)
