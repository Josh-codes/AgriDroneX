# 🚀 Deployment Guide for AgriDetector

## Quick Deployment Options

### Option 1: Vercel (Frontend) + Railway (Backend) ⭐ RECOMMENDED

#### **Step 1: Deploy Frontend to Vercel**

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository: `AgriDroneX`
   - Configure:
     - **Framework Preset**: Vite
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
   - Click "Deploy"

3. **Add Environment Variables** in Vercel:
   - Go to Project Settings → Environment Variables
   - Add: `VITE_API_URL` = `your-backend-url-here` (will get this from Railway)

#### **Step 2: Deploy Backend to Railway**

1. **Go to [railway.app](https://railway.app)**
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `AgriDroneX` repository
5. Railway will auto-detect Django

6. **Add Environment Variables**:
   - Click on your service → Variables tab
   - Add these variables:
     ```
     DEBUG=False
     SECRET_KEY=your-super-secret-random-key-here
     ALLOWED_HOSTS=*.railway.app
     OPENWEATHER_API_KEY=your-api-key
     DATABASE_URL=postgresql://... (Railway provides this automatically)
     ```

7. **Add Postgres Database**:
   - In Railway project, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway automatically links it to your app

8. **Deploy**:
   - Railway will automatically build and deploy
   - Get your URL from the Deployments tab (e.g., `your-app.railway.app`)

9. **Update Vercel Frontend**:
   - Go back to Vercel project settings
   - Update `VITE_API_URL` to your Railway backend URL

---

### Option 2: Render (Full Stack - FREE)

#### **Frontend Deployment**

1. Go to [render.com](https://render.com)
2. Click "New +" → "Static Site"
3. Connect GitHub repository
4. Configure:
   - **Name**: agridetector-frontend
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
5. Add Environment Variable:
   - `VITE_API_URL` = (backend URL from next step)

#### **Backend Deployment**

1. In Render, click "New +" → "Web Service"
2. Connect same repository
3. Configure:
   - **Name**: agridetector-backend
   - **Root Directory**: Leave blank
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd farmer_weather && python manage.py migrate && gunicorn farmer_weather.wsgi:application`
   - **Environment**: Python 3
4. Add Environment Variables:
   ```
   DEBUG=False
   SECRET_KEY=your-random-secret-key
   ALLOWED_HOSTS=*.onrender.com
   OPENWEATHER_API_KEY=your-api-key
   DATABASE_URL=postgresql://... (from Render PostgreSQL)
   ```
5. Add PostgreSQL Database:
   - Click "New +" → "PostgreSQL"
   - Link to your web service

---

### Option 3: PythonAnywhere (Django) + Netlify (React)

#### **Frontend on Netlify**

1. Go to [netlify.com](https://netlify.com)
2. Drag & drop your `frontend/dist` folder (after running `npm run build`)
3. Or connect GitHub repo:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`

#### **Backend on PythonAnywhere**

1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Create free account
3. Open Bash console
4. Clone repo:
   ```bash
   git clone https://github.com/Josh-codes/AgriDroneX.git
   cd AgriDroneX/farmer_weather
   pip install -r ../requirements.txt
   python manage.py migrate
   python manage.py collectstatic
   ```
5. Configure web app in Web tab
6. Set WSGI file path

---

## 📝 Pre-Deployment Checklist

- [ ] Update `.env` with production values
- [ ] Run `npm run build` in frontend to test
- [ ] Test Django with `DEBUG=False` locally
- [ ] Add `.gitignore` entries for sensitive files
- [ ] Update CORS settings for production domain
- [ ] Get valid OpenWeatherMap API key
- [ ] Set strong SECRET_KEY for Django

---

## 🔒 Security Notes

1. **Never commit**:
   - `.env` files
   - API keys
   - Secret keys
   - Database passwords

2. **Always set in production**:
   - `DEBUG=False`
   - Strong `SECRET_KEY`
   - Proper `ALLOWED_HOSTS`
   - Valid SSL certificate

---

## 🆘 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/

---

## 🎉 After Deployment

1. Test all features on production URL
2. Monitor logs for errors
3. Set up domain name (optional)
4. Configure SSL certificate
5. Set up monitoring/analytics
