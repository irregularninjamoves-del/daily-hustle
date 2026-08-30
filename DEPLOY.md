# Deploying Daily Hustle

## Backend Deployment

### Option 1: Render (Recommended - Free Tier)

1. Create account at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repo
4. Select the `backend` directory
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables:
   - `SECRET_KEY` (generate random string)
   - `DATABASE_URL` (Render will auto-create PostgreSQL)
8. Deploy!

### Option 2: Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Init: `railway init`
4. Deploy: `railway up`

### Option 3: Fly.io

```bash
cd backend
fly launch
fly deploy
```

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. Push code to GitHub
2. Connect repo to [vercel.com](https://vercel.com)
3. Set root directory to `frontend`
4. Add environment variable:
   - `VITE_API_URL` = your backend URL
5. Deploy!

### Option 2: Netlify

1. Build locally: `cd frontend && npm run build`
2. Drag `dist` folder to Netlify
3. Or connect GitHub for auto-deploy

### Option 3: GitHub Pages

```bash
cd frontend
npm run build
# Copy dist to docs folder for GitHub Pages
```

## Complete Deployment Checklist

### Backend
- [ ] Environment variables set
- [ ] Database migrated
- [ ] Seed data loaded
- [ ] Health check passing
- [ ] CORS configured for frontend domain

### Frontend
- [ ] API URL environment variable set
- [ ] Build successful
- [ ] PWA manifest valid
- [ ] Service worker registered
- [ ] Icons generated (192x192, 512x512)

### ML Features
- [ ] Initial training run completed
- [ ] Scheduler configured for daily retraining
- [ ] User vectors stored correctly

### Notifications
- [ ] VAPID keys generated
- [ ] Push service configured
- [ ] Subscription storage working

## VAPID Key Generation

For push notifications, generate VAPID keys:

```bash
pip install pywebpush
vapid --gen
```

Copy the private key to your environment variables as `VAPID_PRIVATE_KEY`.

## Testing Deployment

1. Visit frontend URL
2. Register new account
3. Browse deals
4. Check ML recommendations
5. Test push notifications
6. Verify GPS features

## Monitoring

- Backend health: `GET /health`
- API docs: `GET /docs`
- Admin dashboard: `GET /api/admin/dashboard`

## Troubleshooting

**CORS errors**: Add frontend domain to backend CORS settings

**Database errors**: Check DATABASE_URL format

**ML not working**: Run initial training: `python -c "from app.ml.trainer import retrain_all; import asyncio; asyncio.run(retrain_all())"`

**Push notifications**: Verify VAPID keys are set correctly
