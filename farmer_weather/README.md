# Farmer Weather App

A Django-based weather application designed specifically for farmers. This app helps farmers make informed decisions by providing weather forecasts, crop-specific insights, and intelligent recommendations based on local weather conditions.

## Features

### 🌍 Location Selection
- Interactive Google Maps integration
- Search for any location worldwide
- Drag-and-drop marker placement
- Automatic address lookup

### 🌾 Crop Management
- Support for multiple crop types (Tomato, Potato, Pepper, Wheat, Rice, Corn, Cotton, Soybean)
- Crop-specific optimal conditions
- Water requirement tracking
- Frost tolerance monitoring

### ☀️ Weather Information
- Real-time current weather data
- 5-day detailed forecast
- Temperature, humidity, wind speed, and precipitation
- Weather condition descriptions

### 💡 Intelligent Insights
- **Watering Recommendations**: Smart irrigation guidance based on rainfall and crop needs
- **Planting Advice**: Optimal planting window detection
- **Weather Warnings**: Alerts for frost, extreme temperatures, and heavy rain
- **Harvesting Tips**: Best time suggestions for harvest
- Priority-based recommendations (High, Medium, Low)

### 📅 Weather Calendar
- Visual 5-day weather calendar
- Daily weather summaries
- Hourly breakdowns
- Activity planning suggestions

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- OpenWeatherMap API key (free tier available)
- Google Maps API key

### Step 1: Clone or Download

Download the project to your local machine.

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```

2. Edit `.env` file and add your API keys:
   ```
   SECRET_KEY=your-django-secret-key
   OPENWEATHER_API_KEY=your-openweathermap-key
   GOOGLE_MAPS_API_KEY=your-google-maps-key
   ```

#### Getting API Keys:

**OpenWeatherMap API:**
1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Generate an API key (free tier includes 1,000 calls/day)

**Google Maps API:**
1. Visit https://console.cloud.google.com/
2. Create a new project
3. Enable Maps JavaScript API and Places API
4. Create credentials (API key)

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 7: Populate Crop Data

```bash
python manage.py shell < populate_crops.py
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 in your browser.

## Usage

### Adding a Farm

1. Click "Add New Farm" on the home page
2. Use the map to select your farm location:
   - Search for a location using the search box
   - Click anywhere on the map
   - Drag the marker to adjust position
3. Enter a farm name
4. Select your crop from the dropdown
5. Click "Create Farm"

### Viewing Weather Dashboard

1. Click on a farm from the home page
2. View current weather conditions
3. Check farming insights and recommendations
4. Review the 5-day forecast

### Using Weather Calendar

1. From the farm dashboard, click "Weather Calendar"
2. View day-by-day weather predictions
3. See hourly breakdowns for each day
4. Use recommendations to plan activities

### Editing a Farm

1. Go to the farm dashboard
2. Click "Edit"
3. Update location, name, or crop
4. Save changes

## Project Structure

```
farmer_weather/
├── farmer_weather/          # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── weather/                 # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URLs
│   ├── admin.py             # Admin configuration
│   ├── weather_service.py   # Weather API integration
│   └── insights.py          # Insight generation logic
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── weather/             # Weather app templates
├── static/                  # Static files
│   └── css/
│       └── style.css        # Custom styles
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables example
└── README.md                # This file
```

## Database Models

### Crop
- Name and type
- Optimal temperature range
- Optimal humidity range
- Water requirements
- Frost tolerance
- Growing season duration

### Farm
- Name and location (coordinates)
- Associated crop
- Creation/update timestamps

### WeatherData
- Temperature, humidity, pressure
- Wind speed and precipitation
- Weather conditions
- Timestamp and farm reference

### FarmingInsight
- Insight type (Watering, Planting, Warning, etc.)
- Title and description
- Priority level
- Valid date range

## Features Explained

### Weather Insights

The app generates intelligent recommendations by analyzing:
- **Rainfall patterns**: Suggests irrigation schedules
- **Temperature ranges**: Checks against crop-optimal temperatures
- **Frost risk**: Warns about freezing conditions
- **Planting windows**: Identifies favorable conditions
- **Watering needs**: Balances rainfall and crop requirements

### Weather Calendar

Provides a visual overview of:
- Daily high/low temperatures
- Precipitation forecasts
- Hourly weather changes
- Activity recommendations

## API Information

### OpenWeatherMap
- **Current Weather API**: Real-time weather data
- **5-Day Forecast API**: 3-hour interval forecasts
- Free tier: 1,000 calls/day, 60 calls/minute

### Google Maps
- **Maps JavaScript API**: Interactive maps
- **Places API**: Location search and autocomplete
- **Geocoding API**: Reverse geocoding for addresses

## Troubleshooting

### No weather data showing
- Check if OPENWEATHER_API_KEY is correctly set in .env
- Ensure you have internet connectivity
- Verify API key is active (may take a few hours after creation)

### Map not loading
- Check if GOOGLE_MAPS_API_KEY is correctly set in .env
- Enable required APIs in Google Cloud Console
- Check browser console for errors

### Database errors
- Run `python manage.py migrate` again
- Delete db.sqlite3 and run migrations from scratch

## Future Enhancements

- [ ] Historical weather data tracking
- [ ] Soil moisture predictions
- [ ] Pest and disease alerts based on weather
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] SMS/Email notifications
- [ ] Integration with IoT sensors
- [ ] Crop yield predictions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please create an issue in the repository.

## Acknowledgments

- Weather data powered by OpenWeatherMap
- Maps powered by Google Maps Platform
- Built with Django framework
- UI components from Bootstrap 5

---

**Happy Farming! 🌾🚜**
