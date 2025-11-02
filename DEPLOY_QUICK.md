# 🚀 Quick Deploy - AgriDetector

## Fastest Way to Deploy (5 minutes)

### 1️⃣ Deploy Frontend (Vercel - FREE)

```bash
# In the frontend directory
cd frontend
npm run build
```

Then:
1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import from GitHub: `AgriDroneX`
4. Settings:
   - Root Directory: `frontend`
   - Framework: Vite
   - Build: `npm run build`
   - Output: `dist`
5. Click "Deploy"
6. ✅ Frontend is live!

### 2️⃣ Deploy Backend (Railway - FREE)

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose `AgriDroneX`
5. Add PostgreSQL database (click "+ New" → "Database")
6. Add environment variables:
   ```
   DEBUG=False
   SECRET_KEY=make-this-random-and-long
   ALLOWED_HOSTS=*.railway.app
   OPENWEATHER_API_KEY=your-api-key
   ```
7. ✅ Backend is live!

### 3️⃣ Connect Them

1. Copy your Railway backend URL (e.g., `https://agridetector.railway.app`)
2. In Vercel project settings → Environment Variables:
   - Add: `VITE_API_URL` = `https://agridetector.railway.app`
3. Redeploy frontend in Vercel
4. ✅ Done!

---

## 📱 Your Live URLs

- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://your-project.railway.app`

---

## 🔑 Important: Get Your API Key

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up (free)
3. Generate API key
4. Add to Railway environment variables
5. Wait 1-2 hours for activation

---

## ✅ Verify Deployment

Test these URLs:
- Frontend: `https://your-project.vercel.app`
- Backend API: `https://your-project.railway.app/admin`
- Weather API: `https://your-project.railway.app/api/farms/`

---

## 💡 Pro Tips

- **Free Tier Limits**:
  - Vercel: Unlimited bandwidth
  - Railway: 500 hours/month free
  
- **Custom Domain**: Add in Vercel/Railway settings

- **Monitor**: Check Railway logs for errors

- **Update**: Just push to GitHub, auto-deploys!

---

## 🆘 Troubleshooting

**Frontend shows blank page?**
- Check browser console for API errors
- Verify `VITE_API_URL` is set correctly

**Backend 500 error?**
- Check Railway logs
- Verify DATABASE_URL is set
- Run migrations: `python manage.py migrate`

**Weather data not showing?**
- Check OpenWeather API key is valid
- Wait 1-2 hours after creating key
- Test API directly: `https://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid=YOUR_KEY`

---

Need detailed instructions? See [DEPLOYMENT.md](./DEPLOYMENT.md)
