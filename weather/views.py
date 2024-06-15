from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import WeatherRecord, WeatherStatistics
from .serializers import WeatherRecordSerializer, WeatherStatisticsSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from datetime import datetime
import yaml

def swagger_schema(request):
    """Retrieves the Swagger schema from the './schema.yaml' file and returns it as a JSON response."""
    with open('./schema.yaml', 'r') as f:
        schema = yaml.safe_load(f)
    return JsonResponse(schema)

class StandardResultsSetPagination(PageNumberPagination):
    """Pagination class for the WeatherRecordList and WeatherStatisticsList views."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class WeatherRecordList(generics.ListAPIView):
    serializer_class = WeatherRecordSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Retrieves a queryset of WeatherRecord objects filtered by optional 'date' and 'station' parameters."""
        queryset = WeatherRecord.objects.all().order_by('id')
        date = self.request.query_params.get('date', None)
        station = self.request.query_params.get('station', None)
        if date and not station:
            try:
                # Validate the date format
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError({'date': 'Invalid date format. Use YYYY-MM-DD.'})
            queryset = queryset.filter(date=date)
        if station and not date:
            queryset = queryset.filter(station_id=station)
        if date and station:
            queryset = queryset.filter(date=date, station_id=station)
        return queryset

class WeatherStatisticsList(generics.ListAPIView):
    serializer_class = WeatherStatisticsSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """ Retrieves the queryset of WeatherStatistics objects with optional filtering by year and station."""
        queryset = WeatherStatistics.objects.all().order_by('id')
        year = self.request.query_params.get('year', None)
        station = self.request.query_params.get('station', None)
        if year and not station:
            queryset = queryset.filter(year=year)
        if station and not year:
            queryset = queryset.filter(station_id=station)
        if station and year:
            queryset = queryset.filter(year=year, station_id=station)
        return queryset
