from django.db import models
from django.contrib.auth.models import User


class Crop(models.Model):
    """Model representing different crop types with their growing characteristics"""
    CROP_TYPES = [
        ('TOMATO', 'Tomato'),
        ('POTATO', 'Potato'),
        ('PEPPER', 'Pepper (Bell)'),
        ('WHEAT', 'Wheat'),
        ('RICE', 'Rice'),
        ('CORN', 'Corn'),
        ('COTTON', 'Cotton'),
        ('SOYBEAN', 'Soybean'),
    ]
    
    name = models.CharField(max_length=100, choices=CROP_TYPES, unique=True)
    optimal_temp_min = models.FloatField(help_text="Minimum optimal temperature in Celsius")
    optimal_temp_max = models.FloatField(help_text="Maximum optimal temperature in Celsius")
    optimal_humidity_min = models.FloatField(help_text="Minimum optimal humidity percentage")
    optimal_humidity_max = models.FloatField(help_text="Maximum optimal humidity percentage")
    water_requirement = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ])
    frost_tolerance = models.BooleanField(default=False)
    growing_season_days = models.IntegerField(help_text="Average days to harvest")
    
    def __str__(self):
        return self.get_name_display()


class Farm(models.Model):
    """Model representing a farmer's location and crop selection"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=300)
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.location_name}"


class WeatherData(models.Model):
    """Model to cache weather data"""
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='weather_records')
    timestamp = models.DateTimeField()
    temperature = models.FloatField(help_text="Temperature in Celsius")
    feels_like = models.FloatField(help_text="Feels like temperature in Celsius")
    humidity = models.FloatField(help_text="Humidity percentage")
    pressure = models.FloatField(help_text="Atmospheric pressure in hPa")
    wind_speed = models.FloatField(help_text="Wind speed in m/s")
    precipitation = models.FloatField(default=0, help_text="Precipitation in mm")
    weather_condition = models.CharField(max_length=100)
    weather_description = models.CharField(max_length=200)
    clouds = models.FloatField(help_text="Cloudiness percentage")
    fetched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        
    def __str__(self):
        return f"{self.farm.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class FarmingInsight(models.Model):
    """Model to store farming recommendations and insights"""
    INSIGHT_TYPES = [
        ('WATERING', 'Watering Recommendation'),
        ('PLANTING', 'Planting Recommendation'),
        ('HARVESTING', 'Harvesting Recommendation'),
        ('WARNING', 'Weather Warning'),
        ('GENERAL', 'General Advice'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='insights')
    insight_type = models.CharField(max_length=20, choices=INSIGHT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.IntegerField(default=1, help_text="1=Low, 2=Medium, 3=High")
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority', 'valid_from']
        
    def __str__(self):
        return f"{self.farm.name} - {self.title}"
