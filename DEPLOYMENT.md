# Deployment Guide

This guide covers how to deploy the JobFlowAI application locally (using Docker Compose) and to cloud platforms.

## Prerequisites
- Docker & Docker Compose installed
- Git installed
- Python 3.11+ (for local dev without Docker)
- Node.js 18+ (for local dev without Docker)

## 1. Local Deployment (Docker Compose)

The easiest way to run the full stack locally.

### Setup
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Jobflowai
   ```

2. **Environment Variables:**
   - The `docker-compose.yml` file has default values for local development. 
   - Ensure you have a `.env` file in `backend/.env` if you want to override secrets (though for local docker-compose, we use dummy values by default for safety).

### Run
```bash
# Build and start services
docker-compose up -d --build
```

- **Backend API**: http://localhost:8000
- **Database**: `postgres://user:pass@localhost:5432/jobflowai`
- **Frontend** (if enabled in docker-compose): http://localhost:3000

To stop:
```bash
docker-compose down
```

## 2. Production Deployment (Docker Compose)

For deploying to a VPS (single server).

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```
This runs the Nginx frontend, Backend API, and Postgres DB in a production-like configuration.

## 3. Cloud Deployment (Platform as a Service)

### Backend (Render / Railway)
- **Repo Config**: Connect your repository.
- **Root Directory**: `.` (Root)
- **Build Command**: `pip install -r backend/requirements.txt` (if running natively) OR use the Dockerfile.
- **Docker Build Context**: `.` (Root)
- **Dockerfile Path**: `backend/Dockerfile`
- **Environment Variables**:
    - `DATABASE_URL`: Connection string to your cloud Postgres DB.
    - `OPENAI_API_KEY`: Your key.
    - `SECRET_KEY`: A strong random string.
    - `ALLOWED_ORIGINS`: Your frontend URL (e.g., `https://my-app.vercel.app`).

### Frontend (Vercel / Netlify)
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Environment Variables**:
    - `REACT_APP_API_BASE_URL`: Link to your deployed backend (e.g., `https://my-backend.onrender.com/`).

## Troubleshooting
- **"Module not found: 'backend'"**: Ensure your Dockerfile sets `PYTHONPATH=/app` and copies the `backend` folder into `/app/backend`.
- **Database Connection Errors**: Ensure the `DATABASE_URL` is correct and the database service is healthy.
