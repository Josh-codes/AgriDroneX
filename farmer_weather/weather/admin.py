from django.contrib import admin
from .models import Crop, Farm, WeatherData, FarmingInsight


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'optimal_temp_min', 'optimal_temp_max', 'water_requirement']
    list_filter = ['water_requirement', 'frost_tolerance']


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_name', 'crop', 'created_at']
    list_filter = ['crop', 'created_at']
    search_fields = ['name', 'location_name']


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['farm', 'timestamp', 'temperature', 'humidity', 'weather_condition']
    list_filter = ['weather_condition', 'timestamp']
    search_fields = ['farm__name']


@admin.register(FarmingInsight)
class FarmingInsightAdmin(admin.ModelAdmin):
    list_display = ['farm', 'insight_type', 'title', 'priority', 'valid_from']
    list_filter = ['insight_type', 'priority', 'created_at']
    search_fields = ['farm__name', 'title']
