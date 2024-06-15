from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase, Client
from .models import WeatherRecord, WeatherStatistics
import os
from django.urls import reverse


class WeatherRecordListTests(TestCase):
    """Tests for the WeatherRecordList view."""
    def setUp(self):
        self.client = APIClient()
        # Create test data
        WeatherRecord.objects.create(date='2023-06-01', station_id='001', max_temp=30, min_temp=20, precipitation=10)
        WeatherRecord.objects.create(date='2023-06-02', station_id='002', max_temp=32, min_temp=21, precipitation=5)
        WeatherRecord.objects.create(date='2023-06-01', station_id='003', max_temp=33, min_temp=22, precipitation=8)

    def test_filter_by_date(self):
        response = self.client.get('/weather/records/', {'date': '2023-06-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)

    def test_filter_by_station(self):
        response = self.client.get('/weather/records/', {'station': '002'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_filter_by_date_and_station(self):
        response = self.client.get('/weather/records/', {'date': '2023-06-01', 'station': '003'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_filter_by_invalid_date(self):
        response = self.client.get('/weather/records/', {'date': '2023-31-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get('/weather/records/', {'date': '2023/31/01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data.get('results'))

    def test_filter_by_invalid_station(self):
        response = self.client.get('/weather/records/', {'station': '123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_filter_by_date_and_invalid_station(self):
        response = self.client.get('/weather/records/', {'date': '2023-06-01', 'station': '123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 0)

class WeatherStatisticsListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test data
        WeatherStatistics.objects.create(year=2023, station_id='001', avg_max_temp=25.0, avg_min_temp=15.0, total_precipitation=100.0)
        WeatherStatistics.objects.create(year=2024, station_id='002', avg_max_temp=26.5, avg_min_temp=16.5, total_precipitation=80.0)
        WeatherStatistics.objects.create(year=2023, station_id='003', avg_max_temp=27.0, avg_min_temp=17.0, total_precipitation=90.0)

    def test_filter_by_year(self):
        response = self.client.get('/weather/stats/', {'year': '2023'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)

    def test_filter_by_station(self):
        response = self.client.get('/weather/stats/', {'station': '002'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_filter_by_year_and_station(self):
        response = self.client.get('/weather/stats/', {'year': '2023', 'station': '002'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_filter_by_year_and_station_and_date(self):
        response = self.client.get('/weather/stats/', {'year': '2024', 'station': '002'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
    
    def test_filter_by_invalid_year(self):
        response = self.client.get('/weather/stats/', {'year': '123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_filter_by_invalid_station(self):
        response = self.client.get('/weather/stats/', {'station': '123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_filter_by_year_and_invalid_station(self):
        response = self.client.get('/weather/stats/', {'year': '2023', 'station': '123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_filter_by_year_and_station_and_invalid_date(self):
        response = self.client.get('/weather/stats/', {'year': '2024', 'station': '2002', 'date': '2023-06-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 0)
        
    def test_swagger_schema(self):
        response = self.client.get('/weather/api/docs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redoc_schema(self):
        response = self.client.get('/weather/api/redoc/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

