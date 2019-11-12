from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField("Name", max_length=150)

    # Para cambiar el nombre que aparece en el django admin
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def to_dict(self):
        return {
            "name": self.name
        }


class Day(models.Model):
    date= models.DateField("Dia", blank=False, null=False)
    city=models.ForeignKey(City, models.CASCADE, null=False, blank=False)
    update_at=models.DateTimeField("Updated at", null=True, blank=True)

    def __str__(self):
        return f"{self.city.name} {self.date}"

# Los registros de tiempo de cada día
class WeatherRecord(models.Model):
    datetime = models.DateTimeField("Date time", blank=False, null=False)
    temp_max = models.DecimalField("Temp max", max_digits=5, decimal_places=2)
    temp_min = models.DecimalField("Temp min", max_digits=5, decimal_places=2)
    humidity = models.IntegerField("Humidity")
    wind = models.DecimalField("Wind", max_digits=5, decimal_places=2)
    description = models.TextField("Description")
    icon = models.CharField("Icon", max_length=20)
    day = models.ForeignKey(Day, models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.day.city} {self.day.day} {self.datetime}"