# Farmer Weather App - Test Data Script
# This script populates the database with crop data

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmer_weather.settings')
django.setup()

from weather.models import Crop

def create_crops():
    """Create default crop entries"""
    crops_data = [
        {
            'name': 'TOMATO',
            'optimal_temp_min': 18,
            'optimal_temp_max': 29,
            'optimal_humidity_min': 60,
            'optimal_humidity_max': 80,
            'water_requirement': 'MEDIUM',
            'frost_tolerance': False,
            'growing_season_days': 75
        },
        {
            'name': 'POTATO',
            'optimal_temp_min': 15,
            'optimal_temp_max': 20,
            'optimal_humidity_min': 70,
            'optimal_humidity_max': 85,
            'water_requirement': 'MEDIUM',
            'frost_tolerance': True,
            'growing_season_days': 90
        },
        {
            'name': 'PEPPER',
            'optimal_temp_min': 20,
            'optimal_temp_max': 30,
            'optimal_humidity_min': 60,
            'optimal_humidity_max': 75,
            'water_requirement': 'MEDIUM',
            'frost_tolerance': False,
            'growing_season_days': 70
        },
        {
            'name': 'WHEAT',
            'optimal_temp_min': 12,
            'optimal_temp_max': 25,
            'optimal_humidity_min': 50,
            'optimal_humidity_max': 70,
            'water_requirement': 'LOW',
            'frost_tolerance': True,
            'growing_season_days': 120
        },
        {
            'name': 'RICE',
            'optimal_temp_min': 20,
            'optimal_temp_max': 35,
            'optimal_humidity_min': 80,
            'optimal_humidity_max': 90,
            'water_requirement': 'HIGH',
            'frost_tolerance': False,
            'growing_season_days': 120
        },
        {
            'name': 'CORN',
            'optimal_temp_min': 18,
            'optimal_temp_max': 32,
            'optimal_humidity_min': 60,
            'optimal_humidity_max': 75,
            'water_requirement': 'MEDIUM',
            'frost_tolerance': False,
            'growing_season_days': 90
        },
        {
            'name': 'COTTON',
            'optimal_temp_min': 21,
            'optimal_temp_max': 35,
            'optimal_humidity_min': 50,
            'optimal_humidity_max': 65,
            'water_requirement': 'MEDIUM',
            'frost_tolerance': False,
            'growing_season_days': 150
        },
        {
            'name': 'SOYBEAN',
            'optimal_temp_min': 20,
            'optimal_temp_max': 30,
            'optimal_humidity_min': 60,
            'optimal_humidity_max': 75,
            'water_requirement': 'MEDIUM',
            'frost_tolerance': False,
            'growing_season_days': 100
        },
    ]
    
    created_count = 0
    for crop_data in crops_data:
        crop, created = Crop.objects.get_or_create(
            name=crop_data['name'],
            defaults=crop_data
        )
        if created:
            created_count += 1
            print(f"Created crop: {crop.get_name_display()}")
        else:
            print(f"Crop already exists: {crop.get_name_display()}")
    
    print(f"\nTotal crops created: {created_count}")
    print(f"Total crops in database: {Crop.objects.count()}")

if __name__ == '__main__':
    create_crops()
