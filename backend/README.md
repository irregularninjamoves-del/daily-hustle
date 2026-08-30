# Daily Hustle Backend

FastAPI backend for the Daily Hustle app - an AI-powered daily deals and side hustle finder.

## Features

- **Coupons & Deals**: Real-time scraping from coupon sites
- **Side Hustles**: Curated directory of gig economy opportunities
- **Delivery Services**: Bike-friendly delivery options
- **GPS Integration**: Location-aware deal recommendations
- **ML Recommendations**: Personalized feed based on user behavior
- **PWA Support**: Full mobile app experience

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize database and seed data:
```bash
python seed_data.py
```

3. Run the server:
```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

- `/api/auth` - Authentication
- `/api/coupons` - Coupon management
- `/api/hustles` - Side hustle listings
- `/api/delivery` - Delivery services
- `/api/location` - GPS and geolocation features
