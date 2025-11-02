import requests
from datetime import datetime, timedelta
from django.conf import settings
from .models import WeatherData, Farm


class WeatherService:
    """Service to fetch and process weather data from OpenWeatherMap API"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
    
    def get_current_weather(self, lat, lon):
        """Fetch current weather data"""
        url = f"{self.BASE_URL}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching current weather: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            return None
    
    def get_forecast(self, lat, lon, days=5):
        """Fetch weather forecast data"""
        url = f"{self.BASE_URL}/forecast"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching forecast: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            return None
    
    def save_weather_data(self, farm, weather_json):
        """Save weather data to database"""
        if not weather_json:
            return None
        
        timestamp = datetime.fromtimestamp(weather_json['dt'])
        
        weather_data = WeatherData.objects.create(
            farm=farm,
            timestamp=timestamp,
            temperature=weather_json['main']['temp'],
            feels_like=weather_json['main']['feels_like'],
            humidity=weather_json['main']['humidity'],
            pressure=weather_json['main']['pressure'],
            wind_speed=weather_json['wind']['speed'],
            precipitation=weather_json.get('rain', {}).get('3h', 0) + weather_json.get('snow', {}).get('3h', 0),
            weather_condition=weather_json['weather'][0]['main'],
            weather_description=weather_json['weather'][0]['description'],
            clouds=weather_json['clouds']['all']
        )
        
        return weather_data
    
    def save_forecast_data(self, farm, forecast_json):
        """Save forecast data to database"""
        if not forecast_json or 'list' not in forecast_json:
            return []
        
        # Clear old forecast data
        WeatherData.objects.filter(
            farm=farm,
            timestamp__gte=datetime.now()
        ).delete()
        
        saved_records = []
        for item in forecast_json['list']:
            weather_data = self.save_weather_data(farm, item)
            if weather_data:
                saved_records.append(weather_data)
        
        return saved_records
    
    def get_weather_summary(self, farm):
        """Get weather summary for the farm"""
        current = self.get_current_weather(farm.latitude, farm.longitude)
        forecast = self.get_forecast(farm.latitude, farm.longitude)
        
        if current:
            self.save_weather_data(farm, current)
        
        if forecast:
            self.save_forecast_data(farm, forecast)
        
        return {
            'current': current,
            'forecast': forecast
        }
