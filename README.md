# AgriDroneX - Smart Crop Technology Platform

A full-stack application for precision agriculture using drone technology to provide insights to farmers. The platform includes weather monitoring, crop disease detection using ML, and comprehensive farm management.

## Features

- **Home Page**: Modern landing page with hero section, features, and footer
- **Services Page**: Pricing plans (Standard & Premium) with expandable features
- **Weather Dashboard**: Integrated weather monitoring for farms with location-based data
- **Crop Disease Detection**: ML-powered image analysis for crop blight detection
- **AI Chatbot**: Gemini-powered agricultural assistant for crop recommendations and farming advice
- **Insights/FAQ**: Comprehensive FAQ section
- **Responsive Design**: Modern, clean UI matching the provided designs

## Tech Stack

### Frontend
- React 18
- React Router DOM
- Vite
- Axios
- CSS3

### Backend
- Django 4.2
- Django REST Framework (via API views)
- TensorFlow (for ML model)
- OpenCV (for image processing)
- SQLite (database)

## Project Structure

```
Agridetector/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable components (Navbar, ChatButton)
│   │   ├── pages/           # Page components (Home, Services, Weather, etc.)
│   │   ├── App.jsx          # Main app component with routing
│   │   └── main.jsx         # Entry point
│   ├── package.json
│   └── vite.config.js
│
└── farmer_weather/          # Django backend
    ├── weather/
    │   ├── api_views.py      # API endpoints for React frontend
    │   ├── views.py          # Django template views (legacy)
    │   ├── models.py         # Database models
    │   ├── urls.py           # URL routing
    │   └── weather_service.py # Weather API integration
    ├── farmer_weather/
    │   ├── settings.py       # Django settings
    │   └── urls.py           # Root URL config
    └── tomato_blight_model.keras  # ML model for disease detection
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup (Django)

1. Navigate to the Django project directory:
```bash
cd farmer_weather
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the `farmer_weather` directory:
```
OPENWEATHER_API_KEY=your_openweather_api_key_here
SECRET_KEY=your_secret_key_here
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Populate crops data (optional):
```bash
python populate_crops.py
```

7. Start the Django server:
```bash
python manage.py runserver
```

The backend will run on `http://localhost:8000`

### Frontend Setup (React)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## API Endpoints

### Weather API
- `GET /api/farms/` - Get all farms
- `POST /api/farms/` - Create a new farm
- `DELETE /api/farms/<id>/` - Delete a farm
- `GET /api/farms/<id>/weather/` - Get weather data for a farm
- `GET /api/crops/` - Get all available crops

### ML Prediction API
- `POST /api/predict/` - Upload image for crop blight detection
  - Request: multipart/form-data with `image` field
  - Response: JSON with prediction results

### Chatbot API
- `POST /api/chat/` - Chat with Gemini AI agricultural assistant
  - Request: JSON with `message` (required) and `location` (optional)
  - Response: JSON with AI response
  - Features: Location-based crop recommendations, farming advice, disease prevention tips

## Usage

1. **Home Page**: Navigate to the root URL to see the landing page
2. **Services**: Click "Services" in the navbar or "Explore Services" button to view pricing plans
3. **Weather**: Click "Weather" in the navbar to access the weather dashboard
   - Add a farm with location (latitude/longitude) and crop type
   - View current weather and 5-day forecast
   - Get farming insights based on weather conditions
4. **Disease Detection**: Click "Get Started" on any service plan to upload crop images
   - Upload an image of your crop
   - Get analysis results with recommendations

## ML Model

The crop blight detection uses a TensorFlow/Keras model (`tomato_blight_model.keras`). The system:
- First attempts to use the ML model for predictions
- Falls back to heuristic color-based analysis if model is unavailable
- Provides confidence scores and recommendations

## Development Notes

- CORS is configured to allow requests from `http://localhost:3000`
- The frontend proxies API requests to `/api/` which are forwarded to Django
- Static files are served by Django in production
- The ML model should be placed in `farmer_weather/tomato_blight_model.keras`

## Future Enhancements

- User authentication
- Farm management dashboard
- Historical data analysis
- Advanced ML model training
- Real-time drone data integration
- Mobile app support

## License

This project is part of the AgriDroneX platform for precision agriculture.

