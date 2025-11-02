from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Farm, Crop, WeatherData, FarmingInsight
from .weather_service import WeatherService
from .insights import InsightGenerator
from datetime import datetime
import os

# ML Prediction imports
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image as kimage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Load ML model
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tomato_blight_model.keras')
model = None
IMG_SIZE = 224

try:
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Loaded ML model:", MODEL_PATH)
    else:
        print("⚠️ ML model not found at", MODEL_PATH, "- will use heuristic fallback")
except Exception as e:
    print(f"⚠️ Error loading ML model: {e}")


def heuristic_blight_check(img_path):
    """Heuristic method to detect blight using color analysis"""
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Image not found or unreadable: {img_path}")
    
    img_small = cv2.resize(img, (256, 256))
    hsv = cv2.cvtColor(img_small, cv2.COLOR_BGR2HSV)
    
    # Brown/yellow color range for blight symptoms
    lower = np.array([5, 50, 50])
    upper = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    
    # Clean up mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    ratio = np.count_nonzero(mask) / (256 * 256)
    is_blight = ratio > 0.02  # 2% threshold
    
    return is_blight, ratio


@csrf_exempt
@require_http_methods(["POST"])
def predict_blight(request):
    """API endpoint for crop blight prediction"""
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image file provided'}, status=400)
    
    uploaded_file = request.FILES['image']
    
    # Save uploaded file temporarily
    file_name = default_storage.save(f'temp/{uploaded_file.name}', ContentFile(uploaded_file.read()))
    file_path = default_storage.path(file_name)
    
    try:
        result = None
        
        # Try ML model prediction first
        if model is not None:
            try:
                img = kimage.load_img(file_path, target_size=(IMG_SIZE, IMG_SIZE))
                x = kimage.img_to_array(img) / 255.0
                x = np.expand_dims(x, 0)
                preds = model.predict(x, verbose=0)
                
                # Handle different model output formats
                if isinstance(preds, list) or isinstance(preds, tuple):
                    disease_pred = preds[0]
                else:
                    disease_pred = preds
                
                prob = float(disease_pred[0][0]) if len(disease_pred[0]) > 0 else float(disease_pred[0])
                is_blight = prob >= 0.5
                label = "Blight" if is_blight else "Not Blight"
                
                result = {
                    'method': 'model',
                    'is_blight': bool(is_blight),
                    'prob': float(prob),
                    'label': label
                }
            except Exception as e:
                print(f"Model prediction failed: {e}, falling back to heuristic")
        
        # Fallback to heuristic if model fails or not available
        if result is None:
            is_blight, ratio = heuristic_blight_check(file_path)
            result = {
                'method': 'heuristic',
                'is_blight': bool(is_blight),
                'score': float(ratio),
                'label': 'Blight (heuristic)' if is_blight else 'Not Blight (heuristic)'
            }
        
        # Clean up temporary file
        default_storage.delete(file_name)
        
        return JsonResponse(result)
        
    except Exception as e:
        # Clean up on error
        if default_storage.exists(file_name):
            default_storage.delete(file_name)
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def get_farms(request):
    """Get all farms or create a new one"""
    if request.method == 'GET':
        farms = Farm.objects.all().order_by('-created_at')
        farms_data = []
        for farm in farms:
            farms_data.append({
                'id': farm.id,
                'name': farm.name,
                'location_name': farm.location_name,
                'latitude': farm.latitude,
                'longitude': farm.longitude,
                'crop': farm.crop.get_name_display() if farm.crop else None,
            })
        return JsonResponse(farms_data, safe=False)
    
    elif request.method == 'POST':
        """Create a new farm"""
        try:
            data = json.loads(request.body)
            crop_id = data.get('crop')
            crop = Crop.objects.get(id=crop_id) if crop_id else None
            
            farm = Farm.objects.create(
                name=data.get('name'),
                latitude=float(data.get('latitude')),
                longitude=float(data.get('longitude')),
                location_name=data.get('location_name'),
                crop=crop
            )
            
            return JsonResponse({
                'id': farm.id,
                'name': farm.name,
                'location_name': farm.location_name,
                'latitude': farm.latitude,
                'longitude': farm.longitude,
                'crop': farm.crop.get_name_display() if farm.crop else None,
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def get_farm_weather(request, farm_id):
    """Get weather data for a specific farm"""
    try:
        farm = Farm.objects.get(id=farm_id)
        
        # Fetch fresh weather data
        weather_service = WeatherService()
        weather_summary = weather_service.get_weather_summary(farm)
        
        # Get stored weather data
        current_weather = WeatherData.objects.filter(
            farm=farm,
            timestamp__lte=datetime.now()
        ).order_by('-timestamp').first()
        
        forecast_data = WeatherData.objects.filter(
            farm=farm,
            timestamp__gte=datetime.now()
        ).order_by('timestamp')[:40]
        
        # Get insights
        insight_generator = InsightGenerator()
        insights = insight_generator.generate_insights(farm)
        
        active_insights = FarmingInsight.objects.filter(
            farm=farm,
            valid_until__gte=datetime.now()
        ).order_by('-priority', 'valid_from')
        
        # Format response
        response_data = {
            'location': farm.location_name,
            'current': {
                'temperature': current_weather.temperature if current_weather else weather_summary.get('temp', 0),
                'feels_like': current_weather.feels_like if current_weather else weather_summary.get('feels_like', 0),
                'humidity': current_weather.humidity if current_weather else weather_summary.get('humidity', 0),
                'pressure': current_weather.pressure if current_weather else weather_summary.get('pressure', 0),
                'wind_speed': current_weather.wind_speed if current_weather else weather_summary.get('wind_speed', 0),
                'weather_condition': current_weather.weather_condition if current_weather else weather_summary.get('condition', 'Unknown'),
                'weather_description': current_weather.weather_description if current_weather else weather_summary.get('description', 'Unknown'),
            },
            'forecast': [
                {
                    'timestamp': w.timestamp.isoformat(),
                    'temperature': w.temperature,
                    'humidity': w.humidity,
                    'weather_condition': w.weather_condition,
                    'weather_description': w.weather_description,
                    'precipitation': w.precipitation,
                }
                for w in forecast_data
            ],
            'insights': [
                {
                    'title': insight.title,
                    'description': insight.description,
                    'insight_type': insight.get_insight_type_display(),
                    'priority': insight.priority,
                }
                for insight in active_insights[:10]
            ]
        }
        
        return JsonResponse(response_data)
    except Farm.DoesNotExist:
        return JsonResponse({'error': 'Farm not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_farm(request, farm_id):
    """Delete a farm"""
    try:
        farm = Farm.objects.get(id=farm_id)
        farm.delete()
        return JsonResponse({'message': 'Farm deleted successfully'}, status=200)
    except Farm.DoesNotExist:
        return JsonResponse({'error': 'Farm not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_crops(request):
    """Get all available crops"""
    crops = Crop.objects.all()
    crops_data = [{
        'id': crop.id,
        'name': crop.get_name_display(),
    } for crop in crops]
    return JsonResponse(crops_data, safe=False)
