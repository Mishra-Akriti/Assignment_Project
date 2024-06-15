from rest_framework import serializers
from .models import WeatherRecord, WeatherStatistics

class WeatherRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeatherRecord
        fields = ['date', 'station_id', 'max_temp', 'min_temp', 'precipitation']

class WeatherStatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeatherStatistics
        fields = ['year', 'station_id', 'avg_max_temp', 'avg_min_temp', 'total_precipitation']
