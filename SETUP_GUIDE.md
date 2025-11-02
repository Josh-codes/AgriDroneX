# Quick Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

## Step 1: Backend Setup (Django)

1. Navigate to Django directory:
```bash
cd farmer_weather
```

2. Create virtual environment:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in `farmer_weather` folder:
```
OPENWEATHER_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

5. Run migrations:
```bash
python manage.py migrate
```

6. (Optional) Populate crops:
```bash
python populate_crops.py
```

7. Start Django server:
```bash
python manage.py runserver
```
Backend runs on http://localhost:8000

## Step 2: Frontend Setup (React)

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```
Frontend runs on http://localhost:3000

## Important Notes

1. **ML Model**: The `tomato_blight_model.keras` file should be in the `farmer_weather` directory. If missing, the system will use heuristic color-based detection as a fallback.

2. **CORS**: Already configured to allow requests from localhost:3000

3. **API Endpoints**: All API endpoints are prefixed with `/api/` and are automatically proxied from the React frontend to Django backend.

4. **Media Files**: Uploaded images are temporarily stored in `farmer_weather/media/temp/` and automatically deleted after processing.

## Troubleshooting

- **CORS errors**: Make sure `django-cors-headers` is installed and CORS middleware is in settings
- **Model not found**: The system will use heuristic detection if the ML model file is missing
- **Weather API errors**: Ensure OPENWEATHER_API_KEY is set in `.env` file
- **Port conflicts**: Change ports in `vite.config.js` (frontend) or `manage.py runserver 8001` (backend)

