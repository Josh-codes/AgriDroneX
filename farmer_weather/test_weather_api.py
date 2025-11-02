"""
Test script to verify OpenWeatherMap API connection
Run this to check if your API key is working
"""
import os
import sys
import django
import requests

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmer_weather.settings')
django.setup()

from django.conf import settings

def test_api():
    api_key = settings.OPENWEATHER_API_KEY
    
    print("=" * 60)
    print("OpenWeatherMap API Test")
    print("=" * 60)
    print(f"\n1. API Key Status:")
    print(f"   Key configured: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"   Key (first 10 chars): {api_key[:10]}...")
    
    if not api_key:
        print("\n❌ ERROR: No API key found!")
        print("   Add your key to the .env file")
        return
    
    # Test with Mumbai coordinates (from your farm)
    lat = 19.1338
    lon = 72.8510
    
    print(f"\n2. Testing API with coordinates: {lat}, {lon}")
    
    # Test current weather
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }
    
    print(f"\n3. Making request to: {url}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS! API is working!")
            print(f"\n   Location: {data['name']}")
            print(f"   Temperature: {data['main']['temp']}°C")
            print(f"   Weather: {data['weather'][0]['description']}")
            print(f"   Humidity: {data['main']['humidity']}%")
            return True
        elif response.status_code == 401:
            print("\n❌ ERROR: Invalid API key!")
            print("   Your API key is not valid or not activated yet")
            print("   • Wait 1-2 hours if you just created it")
            print("   • Check it at: https://home.openweathermap.org/api_keys")
        elif response.status_code == 429:
            print("\n❌ ERROR: Too many requests!")
            print("   You've exceeded the API rate limit")
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.Timeout:
        print("\n❌ ERROR: Request timed out!")
        print("   Check your internet connection")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Connection failed!")
        print("   Check your internet connection")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
    
    return False

if __name__ == '__main__':
    test_api()
    print("\n" + "=" * 60)
