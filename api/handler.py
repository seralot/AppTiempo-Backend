import datetime as dt 
from typing import List

from django.utils.timezone import now

from db import models

class Handler:

    # def __init__(self, data):
    #     self.data = data

    # Comprueba si existe la ciudad en la DB si no la crea
    def checkCity(self, data):
        city, created = models.City.objects.get_or_create(name=data["city"]["name"])
        return city

    # Comprueba si existe el dia en esa ciudad en la DB, sino existe lo crea
    def main(self, data):
        city = self.checkCity(data)
        for item in data["list"]:
            fecha = item["dt_txt"].split()
            day = self.checkDay(fecha[0], city)
            self.update(city, day, fecha[0], item)

    # Comprueba si existe el día en la DB sino lo crea
    def checkDay(self, fecha, city):
        day, created = models.Day.objects.get_or_create(
            date=fecha,
            city=city,
            defaults={'update_at': now()}
        )
        return day

    # Actualiza el update del día
    def update_day(self, fecha, city):
        dayupdate, created = models.Day.objects.update_or_create(
            date=fecha,
            city=city,
            defaults={'update_at': now()}
        )

    # Actualizamos los registros de tiempo
    def update_weather_records(self, stamp, day, item):
        records, created = models.WeatherRecord.objects.update_or_create(
            datetime=stamp,
            day=day,
            defaults={
                'temp_max':item["main"]["temp_max"],
                'temp_min':item["main"]["temp_min"],
                'humidity':item["main"]["humidity"],
                'wind':item["wind"]["speed"],
                'description':item["weather"][0]["description"],
                'icon':item["weather"][0]["icon"],
            }
        )

    # Comprueba si existe los registros de tiempo de ese día en DB si no la crea
    def check_weather_records(self, stamp, day, item):
        record, created = models.WeatherRecord.objects.get_or_create(
            datetime=stamp,
            day=day,
            defaults={
                'temp_max':item["main"]["temp_max"],
                'temp_min':item["main"]["temp_min"],
                'humidity':item["main"]["humidity"],
                'wind':item["wind"]["speed"],
                'description':item["weather"][0]["description"],
                'icon':item["weather"][0]["icon"],}
        )
    

    def update(self, city, day, fecha, item):
        stamp = dt.datetime.fromtimestamp(item["dt"])
        # Si han pasado 2 horas actualizar los registros de tiempo
        if not day.update_at or (day.update_at.hour - now().hour)>=2:
            # Actualizamos los registros de tiempo
            self.update_weather_records(stamp, day, item)
            # Actualizamos la fecha de update del día con la actual
            self.update_day(fecha, city)
        else:
            # comprobar si existe el tiempo en esa hora en la DB, sino existe se crea
            self.check_weather_records(stamp, day, item)

    # Comprueba si la ciudad o el día ya se encuentran en la DB
    # Si no la encuentra la busca en la API
    def check_db(self, city, day: dt.datetime):
        qs = models.City.objects.filter(name=city).exists()
        
        if not qs:
            return False
    
        cityDB = models.City.objects.get(name=city)
        return models.Day.objects.filter(date=day, city=cityDB).exists()

    def get_weather_records(self, city, day: dt.datetime) -> List[models.WeatherRecord]:
        qc = models.City.objects.get(name=city)
        qs = models.Day.objects.filter(date=day, city=qc).exists()

        if not qs:
            return False
        
        d = models.Day.objects.get(date=day, city=qc)

        print(">>>>>>>>>>>>>>>>>>>>>",[e.temp_max for e in models.WeatherRecord.objects.filter(day = d)] )
        # return models.WeatherRecord.objects.filter(day = d)
        data = []

        for e in models.WeatherRecord.objects.filter(day = d):
            data.append(e.to_dict())

        return data