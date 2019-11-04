from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField("Name", max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class WeatherRecord(models.Model):
    datetime = models.DateTimeField("Date time", blank=False, null=False)
    temp_max = models.DecimalField("Temp max", max_digits=5, decimal_places=2)
    temp_min = models.DecimalField("Temp min", max_digits=5, decimal_places=2)
    humidity = models.IntegerField("Humidity")
    wind = models.DecimalField("Wind", max_digits=5, decimal_places=2)
    description = models.TextField("Description")
    icon = models.CharField("Icon", max_length=20)
    city = models.ForeignKey(City, models.CASCADE, null=False, blank=False)