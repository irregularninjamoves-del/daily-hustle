# Docker Setup

## Quick Start (Local Development)

### Option 1: SQLite (Easiest)
```bash
cd daily-hustle

# Run just the API (uses SQLite, no Postgres needed)
docker compose -f docker-compose.yml -f docker-compose.override.yml up api

# Or shorthand
docker compose up api
```

### Option 2: Full Stack (Postgres + Redis)
```bash
# Start everything
docker compose up -d

# View logs
docker compose logs -f api

# Stop
docker compose down
```

## Production Build

### Build and test locally
```bash
docker build -t daily-hustle-api ./backend

docker run -p 8000:8000 -e SECRET_KEY=test daily-hustle-api
```

### Push to registry
```bash
docker tag daily-hustle-api:latest your-registry/daily-hustle-api:latest
docker push your-registry/daily-hustle-api:latest
```

## Render Deployment

1. Delete existing service (if any)
2. Click "New +" → "Blueprint"
3. Connect GitHub repo
4. Render auto-detects `render.yaml` and builds Docker image

## Railway Deployment

```bash
railway login
railway init
railway up
```

Railway auto-detects `Dockerfile` and builds.

## Fly.io Deployment

```bash
cd backend
fly launch
fly deploy
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `SECRET_KEY` | ✅ | JWT signing key |
| `PYTHON_VERSION` | ❌ | 3.11.0 (Docker sets this) |
| `PORT` | ❌ | Set by platform (8000 default) |

## Commands

```bash
# Rebuild after code changes
docker compose up --build api

# Shell into container
docker compose exec api bash

# Run database migrations (if needed)
docker compose exec api python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"

# View running containers
docker ps

# Check logs
docker logs daily-hustle-api -f
```
