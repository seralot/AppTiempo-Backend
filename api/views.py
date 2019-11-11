import datetime as dt 

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
        print(request.GET)
        city = request.GET['city']
        r=getapi(city)
        data = json.loads(r)

    # Instanciamos la clase handler
        handler = Handler(data)
        handler.main()

        return HttpResponse(r)
