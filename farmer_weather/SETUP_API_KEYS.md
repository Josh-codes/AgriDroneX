# IMPORTANT: API Keys Setup

Before using the farmer weather app, you need to set up your API keys.

## Step 1: Copy the environment file

```powershell
copy .env.example .env
```

## Step 2: Get your API keys

### OpenWeatherMap API Key (Free)
1. Go to https://openweathermap.org/api
2. Click "Sign Up" and create a free account
3. Go to "API keys" section
4. Copy your API key

### Google Maps API Key (Free tier available)
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable these APIs:
   - Maps JavaScript API
   - Places API
   - Geocoding API
4. Go to "Credentials" and create an API key
5. Copy your API key

## Step 3: Edit the .env file

Open the `.env` file and add your keys:

```
SECRET_KEY=your-django-secret-key-here
OPENWEATHER_API_KEY=paste-your-openweathermap-key-here
GOOGLE_MAPS_API_KEY=paste-your-google-maps-key-here
```

## Step 4: Run the server

```powershell
python manage.py runserver
```

## Troubleshooting

### Map not showing?
- Check if GOOGLE_MAPS_API_KEY is set in .env
- Open browser console (F12) to see errors
- Make sure you enabled the required APIs in Google Cloud Console

### No weather data?
- Check if OPENWEATHER_API_KEY is set in .env
- Wait a few hours after creating the key (it takes time to activate)

### No crops in dropdown?
- Run: `python populate_crops.py`
