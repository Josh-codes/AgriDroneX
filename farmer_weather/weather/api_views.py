from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
from .models import Farm, Crop, WeatherData, FarmingInsight
from .weather_service import WeatherService
from .insights import InsightGenerator
from datetime import datetime
import os

# Gemini AI imports
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ google-generativeai not installed. Chatbot will not work.")

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


@csrf_exempt
@require_http_methods(["POST"])
def chat_with_gemini(request):
    """Chat endpoint using Google Gemini AI"""
    if not GEMINI_AVAILABLE:
        return JsonResponse({
            'error': 'Gemini AI is not available. Please install google-generativeai package.'
        }, status=503)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        location = data.get('location', '')  # Optional: latitude, longitude or location name
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Configure Gemini
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return JsonResponse({
                'error': 'Gemini API key not configured. Please set GEMINI_API_KEY in environment variables.'
            }, status=500)
        
        genai.configure(api_key=api_key)
        
        # Create a model instance - try different models in order of preference
        model = None
        selected_model_name = None
        model_names = ['gemini-2.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                selected_model_name = model_name
                print(f"✅ Successfully loaded model: {model_name}")
                break
            except Exception as e:
                print(f"⚠️ Model {model_name} not available: {e}")
                continue
        
        if model is None:
            # Fallback: try to list available models
            try:
                print("🔄 Attempting to list available models...")
                available_models = genai.list_models()
                # Get the first available model that supports generateContent
                for m in available_models:
                    if 'generateContent' in m.supported_generation_methods:
                        # Extract model name from full path like "models/gemini-1.5-flash"
                        model_path = m.name
                        selected_model_name = model_path.split('/')[-1] if '/' in model_path else model_path
                        model = genai.GenerativeModel(selected_model_name)
                        print(f"✅ Using available model: {selected_model_name}")
                        break
            except Exception as e:
                print(f"❌ Error listing models: {e}")
        
        if model is None:
            error_msg = (
                'No suitable Gemini model available. '
                'Please check your API key and model availability. '
                'Available models: gemini-1.5-flash, gemini-1.5-pro, or check your Google AI Studio dashboard.'
            )
            return JsonResponse({'error': error_msg}, status=500)
        
        # Build context-aware prompt
        system_prompt = """You are an expert agricultural advisor for AgriDroneX, a precision agriculture platform. 
        Your role is to provide helpful, accurate, and practical advice about:
        - Crop selection and recommendations based on location, climate, and soil conditions
        - Best practices for farming and agriculture
        - Crop diseases, pests, and their prevention
        - Seasonal planting recommendations
        - Soil management and fertilization
        - Irrigation and water management
        - Modern farming techniques and precision agriculture
        
        Always provide:
        - Clear, concise, and actionable advice
        - Location-specific recommendations when location is provided
        - Scientific and practical information
        - Safety considerations when recommending pesticides or chemicals
        
        If asked about crops suitable for an area, consider:
        - Climate zone and temperature ranges
        - Soil type and pH preferences
        - Water availability
        - Growing season length
        - Market demand and profitability
        
        Be friendly, professional, and helpful. If you don't know something, admit it rather than guessing."""
        
        # Add location context if provided
        location_context = ""
        if location:
            location_context = f"\n\nUser's location context: {location}\nProvide location-specific recommendations when relevant."
        
        # Combine prompts
        full_prompt = f"{system_prompt}{location_context}\n\nUser question: {user_message}\n\nProvide a helpful response:"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        # Extract response text
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        return JsonResponse({
            'response': response_text,
            'model': selected_model_name or 'unknown'
        })
        
    except Exception as e:
        print(f"Error in Gemini chat: {e}")
        return JsonResponse({
            'error': f'Failed to generate response: {str(e)}'
        }, status=500)
