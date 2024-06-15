from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import WeatherRecordList, WeatherStatisticsList, swagger_schema

urlpatterns = [
    path('api/schema/', swagger_schema, name='schema'),
    path('records/', WeatherRecordList.as_view(), name='weather-record-list'),
    path('stats/', WeatherStatisticsList.as_view(), name='weather-statistics-list'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
