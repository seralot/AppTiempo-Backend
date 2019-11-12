from django.contrib import admin

from .models import City
from .models import Day
from .models import WeatherRecord

# Register your models here.

admin.site.register(City)
admin.site.register(Day)
admin.site.register(WeatherRecord)