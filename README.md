# Daily Hustle 🚀

**AI-powered daily deals finder, side hustle directory, and bike delivery opportunities - all in one PWA.**

Built with ❤️ using React + FastAPI + Machine Learning

---

## 🌟 Features

### 💰 Save Money
- **Real-time Coupon Scraping** from top sites (RetailMeNot, Slickdeals, etc.)
- **Location-aware Deals** - Find coupons at stores near you
- **ML-powered Recommendations** - Learns your preferences over time
- **One-tap Code Copy** - Easy access to promo codes

### 💵 Make Money
- **Side Hustle Directory** - Curated list of gigs, freelance work, surveys
- **Bike Delivery Finder** - Which services accept bike couriers in your area
- **Pay Comparison** - Compare earnings across platforms
- **Sign-up Bonuses** - Track current promotions

### 📍 GPS Integration
- **Nearby Store Alerts** - Get notified when you pass a store with active coupons
- **Geofence Notifications** - "You're 300m from Target with a 20% off coupon!"
- **Zone Checker** - See which delivery services operate in your city

### 🤖 Machine Learning
- **Personalized Feed** - TF-IDF + cosine similarity based on your interactions
- **Implicit Feedback** - View, click, save, dismiss actions train the model
- **Exploration vs Exploitation** - 80% personalized + 20% new discoveries
- **Cold Start Handling** - Works immediately, improves over time

### 📱 PWA for Android
- **Install from Browser** - No app store needed
- **Works Offline** - Cached deals work without internet
- **Add to Home Screen** - Behaves like a native app
- **Background Sync** - Push notifications for deal alerts

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18 + TypeScript + Vite + Tailwind CSS |
| **PWA** | Vite PWA Plugin + Workbox |
| **State** | Zustand |
| **Backend** | FastAPI + Python 3.11 |
| **Database** | SQLite (dev) → PostgreSQL (prod) |
| **ML** | scikit-learn + TF-IDF + Cosine Similarity |
| **Scraping** | httpx + BeautifulSoup |
| **Location** | OpenStreetMap Nominatim (free geocoding) |

---

## 📁 Project Structure

```
daily-hustle/
├── backend/               # FastAPI Python backend
│   ├── app/
│   │   ├── api/          # API routes (auth, coupons, hustles, delivery, location)
│   │   ├── models/       # SQLAlchemy database models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── services/     # Scrapers, location utilities
│   │   └── ml/           # ML recommendation engine
│   ├── requirements.txt
│   └── seed_data.py      # Initial data seeding
│
├── frontend/              # React TypeScript PWA
│   ├── src/
│   │   ├── components/   # Layout, navigation
│   │   ├── pages/        # Dashboard, Coupons, Hustles, Delivery, Saved, Profile
│   │   ├── services/     # API client
│   │   ├── stores/       # Zustand state management
│   │   └── hooks/        # Custom React hooks
│   ├── public/           # PWA manifest, icons
│   ├── package.json
│   └── vite.config.ts    # PWA configuration
│
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed database with sample data
python seed_data.py

# Run server
python -m app.main
```

Backend will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 3. Install on Android (PWA)

1. Open `http://localhost:3000` in Chrome on Android
2. Tap "Add to Home Screen" or the install prompt
3. The app now appears on your home screen with full-screen mode
4. Works offline and receives push notifications

---

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Current user

### Coupons
- `GET /api/coupons/` - List coupons (search, filter, location)
- `GET /api/coupons/trending` - Most popular
- `POST /api/coupons/save` - Save coupon

### Side Hustles
- `GET /api/hustles/` - List opportunities
- `GET /api/hustles/bike-friendly` - Bike-friendly gigs

### Delivery Services
- `GET /api/delivery/` - All services
- `GET /api/delivery/bike-friendly` - Bike courier options

### Location
- `POST /api/location/update` - Update user position
- `GET /api/location/nearby-deals` - Deals near location
- `POST /api/location/zone-check` - Which services operate here

---

## 🧠 How the ML Works

1. **Content-Based Filtering** using TF-IDF on:
   - Store names, titles, descriptions
   - Categories and discount types

2. **User Profile Vector** - weighted average of:
   - Viewed items (+0.3)
   - Clicked items (+1.0)
   - Saved items (+3.0)
   - Copied codes (+5.0)
   - Dismissed items (-2.0)

3. **Scoring** = Cosine Similarity × Freshness × Proximity

4. **Daily Retraining** - User vectors updated nightly

---

## 🛣️ Roadmap

- [ ] Real scrapers for RetailMeNot, Slickdeals
- [ ] Push notifications for geofence alerts
- [ ] Interactive map with store pins
- [ ] Delivery earnings heatmap
- [ ] Affiliate link integration
- [ ] iOS Safari PWA support

---

## 📄 License

MIT - Free to use, modify, and distribute!

---

**Built with passion for the hustle.** 💪
