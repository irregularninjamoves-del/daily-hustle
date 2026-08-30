# Push to GitHub & Deploy

## 1. Create GitHub Repo

Go to https://github.com/new and create a new repository called `daily-hustle`

## 2. Push Your Code

Run these commands in your terminal:

```bash
cd C:\Users\james\.cline\data\workspaces\chat\daily-hustle

# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/daily-hustle.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 3. Deploy Backend (Render - Free)

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name**: daily-hustle-api
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"

6. Add Environment Variables:
   - `SECRET_KEY` → generate at https://generate-secret.vercel.app/32
   - `DATABASE_URL` → Render will auto-create PostgreSQL (click "PostgreSQL" in sidebar)

7. Once deployed, copy the URL (e.g., `https://daily-hustle-api.onrender.com`)

## 4. Update Frontend API URL

Edit `frontend/.env.production`:
```
VITE_API_URL=https://daily-hustle-api.onrender.com
```

Commit and push:
```bash
git add frontend/.env.production
git commit -m "Update API URL for production"
git push
```

## 5. Deploy Frontend (Vercel)

1. Go to https://vercel.com/new
2. Import your GitHub repo
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Click "Deploy"

5. Add Environment Variable:
   - Name: `VITE_API_URL`
   - Value: `https://daily-hustle-api.onrender.com` (your backend URL)

6. Click "Deploy"

## 6. Install on Android

1. Visit your Vercel URL on Android Chrome
2. Chrome will prompt "Add to Home Screen"
3. Tap it → App installs!
4. Open from home screen - works like native app!

## Your URLs

| Service | URL |
|---------|-----|
| Frontend (Vercel) | `https://daily-hustle.vercel.app` |
| Backend (Render) | `https://daily-hustle-api.onrender.com` |
| API Docs | `https://daily-hustle-api.onrender.com/docs` |

## Troubleshooting

**CORS Errors**: Add your Vercel domain to backend CORS in `backend/app/main.py`:
```python
allow_origins=["https://daily-hustle.vercel.app", "*"]
```

**Build Failures**: Check Render logs for Python errors

**API Not Connecting**: Verify `VITE_API_URL` is set correctly in Vercel env vars

## Local Development

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py
python -m app.main

# Terminal 2 - Frontend  
cd frontend
npm install
npm run dev
```

Visit: http://localhost:3000
