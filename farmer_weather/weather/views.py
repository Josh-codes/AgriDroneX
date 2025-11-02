from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Farm, Crop, WeatherData, FarmingInsight
from .weather_service import WeatherService
from .insights import InsightGenerator
from datetime import datetime, timedelta
import json


def index(request):
    """Home page - list all farms or create new one"""
    farms = Farm.objects.all().order_by('-created_at')
    return render(request, 'weather/index.html', {'farms': farms})


def create_farm(request):
    """Create a new farm with location and crop selection"""
    if request.method == 'POST':
        name = request.POST.get('name')
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        location_name = request.POST.get('location_name')
        crop_id = request.POST.get('crop')
        
        crop = Crop.objects.get(id=crop_id) if crop_id else None
        
        farm = Farm.objects.create(
            name=name,
            latitude=latitude,
            longitude=longitude,
            location_name=location_name,
            crop=crop
        )
        
        messages.success(request, f'Farm "{name}" created successfully!')
        return redirect('farm_dashboard', farm_id=farm.id)
    
    crops = Crop.objects.all()
    
    return render(request, 'weather/create_farm.html', {
        'crops': crops
    })


def farm_dashboard(request, farm_id):
    """Main dashboard showing weather data and insights"""
    farm = get_object_or_404(Farm, id=farm_id)
    
    # Fetch fresh weather data
    weather_service = WeatherService()
    weather_data = weather_service.get_weather_summary(farm)
    
    # Generate insights
    insight_generator = InsightGenerator()
    insights = insight_generator.generate_insights(farm)
    
    # Get stored weather data
    current_weather = WeatherData.objects.filter(
        farm=farm,
        timestamp__lte=datetime.now()
    ).order_by('-timestamp').first()
    
    forecast_data = WeatherData.objects.filter(
        farm=farm,
        timestamp__gte=datetime.now()
    ).order_by('timestamp')[:40]
    
    # Get insights from database
    active_insights = FarmingInsight.objects.filter(
        farm=farm,
        valid_until__gte=datetime.now()
    ).order_by('-priority', 'valid_from')
    
    return render(request, 'weather/dashboard.html', {
        'farm': farm,
        'current_weather': current_weather,
        'forecast_data': forecast_data,
        'insights': active_insights
    })


def weather_calendar(request, farm_id):
    """Weather calendar view"""
    farm = get_object_or_404(Farm, id=farm_id)
    
    # Get weather data for the next 5 days
    forecast_data = WeatherData.objects.filter(
        farm=farm,
        timestamp__gte=datetime.now(),
        timestamp__lte=datetime.now() + timedelta(days=5)
    ).order_by('timestamp')
    
    # Group by date
    calendar_data = {}
    for weather in forecast_data:
        date_key = weather.timestamp.date()
        if date_key not in calendar_data:
            calendar_data[date_key] = []
        calendar_data[date_key].append(weather)
    
    return render(request, 'weather/calendar.html', {
        'farm': farm,
        'calendar_data': calendar_data
    })


def edit_farm(request, farm_id):
    """Edit farm details"""
    farm = get_object_or_404(Farm, id=farm_id)
    
    if request.method == 'POST':
        farm.name = request.POST.get('name')
        farm.latitude = float(request.POST.get('latitude'))
        farm.longitude = float(request.POST.get('longitude'))
        farm.location_name = request.POST.get('location_name')
        crop_id = request.POST.get('crop')
        farm.crop = Crop.objects.get(id=crop_id) if crop_id else None
        farm.save()
        
        messages.success(request, 'Farm updated successfully!')
        return redirect('farm_dashboard', farm_id=farm.id)
    
    crops = Crop.objects.all()
    
    return render(request, 'weather/edit_farm.html', {
        'farm': farm,
        'crops': crops
    })


def delete_farm(request, farm_id):
    """Delete a farm"""
    farm = get_object_or_404(Farm, id=farm_id)
    
    if request.method == 'POST':
        farm.delete()
        messages.success(request, 'Farm deleted successfully!')
        return redirect('index')
    
    return render(request, 'weather/delete_farm.html', {'farm': farm})


def system_check(request):
    """System configuration check"""
    return render(request, 'weather/system_check.html', {
        'openweather_key': settings.OPENWEATHER_API_KEY,
        'crop_count': Crop.objects.count()
    })
