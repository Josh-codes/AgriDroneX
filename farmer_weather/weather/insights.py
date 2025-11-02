from datetime import datetime, timedelta
from .models import FarmingInsight, Farm, WeatherData


class InsightGenerator:
    """Generate farming insights based on weather conditions and crop requirements"""
    
    def generate_insights(self, farm):
        """Generate all insights for a farm"""
        if not farm.crop:
            return []
        
        insights = []
        weather_data = WeatherData.objects.filter(
            farm=farm,
            timestamp__gte=datetime.now()
        ).order_by('timestamp')[:40]  # Next 5 days (8 records per day)
        
        if not weather_data:
            return insights
        
        # Clear old insights
        FarmingInsight.objects.filter(
            farm=farm,
            valid_until__lt=datetime.now()
        ).delete()
        
        # Clear ALL existing insights for this farm to avoid duplicates
        FarmingInsight.objects.filter(farm=farm).delete()
        
        # Generate various insights
        insights.extend(self._check_rainfall(farm, weather_data))
        insights.extend(self._check_temperature(farm, weather_data))
        insights.extend(self._check_frost(farm, weather_data))
        insights.extend(self._check_planting_window(farm, weather_data))
        insights.extend(self._check_watering_needs(farm, weather_data))
        
        return insights
    
    def _check_rainfall(self, farm, weather_data):
        """Check for rainfall and provide recommendations"""
        insights = []
        rainy_days = []
        
        # Convert to list to avoid queryset issues
        weather_list = list(weather_data)
        
        for weather in weather_list:
            if weather.precipitation > 2 or 'rain' in weather.weather_condition.lower():
                rainy_days.append(weather.timestamp.date())
        
        if len(rainy_days) >= 3:
            # Multiple rainy days expected
            insight = FarmingInsight.objects.create(
                farm=farm,
                insight_type='WATERING',
                title='Heavy Rainfall Expected',
                description=f'Rain is expected for {len(rainy_days)} days in the next 5 days. '
                           f'You can skip irrigation during this period. Ensure proper drainage '
                           f'to prevent waterlogging, especially for {farm.crop.name}.',
                priority=2,
                valid_from=datetime.now(),
                valid_until=weather_list[-1].timestamp if weather_list else datetime.now() + timedelta(days=5)
            )
            insights.append(insight)
        elif len(rainy_days) == 0:
            # No rain expected
            insight = FarmingInsight.objects.create(
                farm=farm,
                insight_type='WATERING',
                title='No Rainfall Expected',
                description=f'No significant rainfall expected in the next 5 days. '
                           f'Ensure regular irrigation for your {farm.crop.name} crop. '
                           f'Water requirement: {farm.crop.water_requirement}.',
                priority=2,
                valid_from=datetime.now(),
                valid_until=weather_list[-1].timestamp if weather_list else datetime.now() + timedelta(days=5)
            )
            insights.append(insight)
        
        return insights
    
    def _check_temperature(self, farm, weather_data):
        """Check temperature conditions"""
        insights = []
        crop = farm.crop
        
        # Convert to list
        weather_list = list(weather_data)
        
        high_temp_days = sum(1 for w in weather_list 
                            if w.temperature > crop.optimal_temp_max)
        low_temp_days = sum(1 for w in weather_list 
                           if w.temperature < crop.optimal_temp_min)
        
        if high_temp_days >= 3:
            insight = FarmingInsight.objects.create(
                farm=farm,
                insight_type='WARNING',
                title='High Temperature Alert',
                description=f'Temperatures above optimal range ({crop.optimal_temp_max}°C) '
                           f'expected for {high_temp_days} days. Increase irrigation frequency '
                           f'and consider shade protection for {crop.name}.',
                priority=3,
                valid_from=datetime.now(),
                valid_until=weather_list[-1].timestamp if weather_list else datetime.now() + timedelta(days=5)
            )
            insights.append(insight)
        
        if low_temp_days >= 3:
            insight = FarmingInsight.objects.create(
                farm=farm,
                insight_type='WARNING',
                title='Low Temperature Alert',
                description=f'Temperatures below optimal range ({crop.optimal_temp_min}°C) '
                           f'expected for {low_temp_days} days. Consider protective measures '
                           f'for {crop.name}.',
                priority=3,
                valid_from=datetime.now(),
                valid_until=weather_list[-1].timestamp if weather_list else datetime.now() + timedelta(days=5)
            )
            insights.append(insight)
        
        return insights
    
    def _check_frost(self, farm, weather_data):
        """Check for frost conditions"""
        insights = []
        
        # Convert to list
        weather_list = list(weather_data)
        
        if not farm.crop.frost_tolerance:
            frost_risk = any(w.temperature < 2 for w in weather_list)
            
            if frost_risk:
                insight = FarmingInsight.objects.create(
                    farm=farm,
                    insight_type='WARNING',
                    title='Frost Risk Warning',
                    description=f'Frost conditions expected! {farm.crop.name} is not frost-tolerant. '
                               f'Take immediate protective measures: cover plants, use frost blankets, '
                               f'or consider temporary heating solutions.',
                    priority=3,
                    valid_from=datetime.now(),
                    valid_until=weather_list[-1].timestamp if weather_list else datetime.now() + timedelta(days=5)
                )
                insights.append(insight)
        
        return insights
    
    def _check_planting_window(self, farm, weather_data):
        """Determine if it's a good time for planting"""
        insights = []
        crop = farm.crop
        
        # Check if conditions are favorable
        avg_temp = sum(w.temperature for w in weather_data[:8]) / min(len(weather_data), 8)
        avg_humidity = sum(w.humidity for w in weather_data[:8]) / min(len(weather_data), 8)
        
        is_temp_good = crop.optimal_temp_min <= avg_temp <= crop.optimal_temp_max
        is_humidity_good = crop.optimal_humidity_min <= avg_humidity <= crop.optimal_humidity_max
        no_extreme_weather = not any(w.wind_speed > 15 for w in weather_data[:8])
        
        if is_temp_good and is_humidity_good and no_extreme_weather:
            insight = FarmingInsight.objects.create(
                farm=farm,
                insight_type='PLANTING',
                title='Favorable Planting Conditions',
                description=f'Current weather conditions are optimal for planting {crop.name}. '
                           f'Temperature: {avg_temp:.1f}°C, Humidity: {avg_humidity:.1f}%. '
                           f'Next few days look promising for seed germination.',
                priority=2,
                valid_from=datetime.now(),
                valid_until=datetime.now() + timedelta(days=3)
            )
            insights.append(insight)
        elif not is_temp_good:
            insight = FarmingInsight.objects.create(
                farm=farm,
                insight_type='PLANTING',
                title='Wait for Better Temperature',
                description=f'Current temperature ({avg_temp:.1f}°C) is outside optimal range '
                           f'({crop.optimal_temp_min}-{crop.optimal_temp_max}°C) for {crop.name}. '
                           f'Consider waiting for more favorable conditions.',
                priority=1,
                valid_from=datetime.now(),
                valid_until=datetime.now() + timedelta(days=3)
            )
            insights.append(insight)
        
        return insights
    
    def _check_watering_needs(self, farm, weather_data):
        """Determine watering recommendations"""
        insights = []
        crop = farm.crop
        
        # Calculate moisture needs based on weather
        next_3_days = weather_data[:24]  # 3 days of data
        avg_temp = sum(w.temperature for w in next_3_days) / len(next_3_days) if next_3_days else 0
        total_rain = sum(w.precipitation for w in next_3_days)
        avg_humidity = sum(w.humidity for w in next_3_days) / len(next_3_days) if next_3_days else 0
        
        water_needed = crop.water_requirement
        
        if total_rain < 5 and avg_humidity < 60 and water_needed == 'HIGH':
            insight = FarmingInsight.objects.create(
                farm=farm,
                insight_type='WATERING',
                title='Increase Irrigation',
                description=f'{crop.name} requires high water. With low rainfall ({total_rain:.1f}mm) '
                           f'and humidity ({avg_humidity:.1f}%) expected, increase irrigation frequency. '
                           f'Best time: Early morning or evening.',
                priority=2,
                valid_from=datetime.now(),
                valid_until=datetime.now() + timedelta(days=3)
            )
            insights.append(insight)
        
        return insights
