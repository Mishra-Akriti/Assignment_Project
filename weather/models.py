from django.db import models

class WeatherRecord(models.Model):
    date = models.DateField()
    station_id = models.CharField(max_length=255, unique=True)
    max_temp = models.IntegerField()
    min_temp = models.IntegerField()
    precipitation = models.IntegerField()

    class Meta:
        unique_together = ('date', 'station_id')

class WeatherStatistics(models.Model):
    year = models.IntegerField()
    station_id = models.CharField(max_length=255, unique=True)
    avg_max_temp = models.FloatField(null=True)
    avg_min_temp = models.FloatField(null=True)
    total_precipitation = models.FloatField(null=True)

    class Meta:
        unique_together = ('year', 'station_id')
