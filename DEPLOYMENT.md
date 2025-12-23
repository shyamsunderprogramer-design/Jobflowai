# JobFlowAI Deployment Guide

This guide provides step-by-step instructions to run JobFlowAI locally and deploy it to a production environment.

## Prerequisites

-   **Git**: For version control.
-   **Docker** & **Docker Compose**: For containerized deployment.
-   **Node.js (v14+)**: For local frontend development (optional if using Docker).
-   **Python (v3.8+)**: For local backend development (optional if using Docker).

---

## 1. Local Development

Running the project manually or with mixed Docker/Local setup is best for development.

### Backend (Docker)
The easiest way to run the backend and database is using Docker Compose.

1.  **Environment Setup**:
    Create a `.env` file in `backend/` (or use the one in root if configured).
    ```bash
    # backend/.env
    ENV=dev
    DATABASE_URL=postgresql://user:pass@db:5432/jobflowai
    OPENAI_API_KEY=your_openai_key
    SECRET_KEY=dev_secret
    ```
    *Note: The `docker-compose.yml` provided in the repo already sets some defaults.*

2.  **Start Backend**:
    From the root directory:
    ```bash
    docker-compose up --build
    ```
    -   Backend API: `http://localhost:8000`
    -   Docs: `http://localhost:8000/docs`

### Frontend (Local)
1.  Navigate to `frontend/`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  **Configure API URL**:
    Create `.env` in `frontend/`:
    ```ini
    REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
    ```
    *(The app defaults to http://127.0.0.1:8000 if not set, which usually works)*

4.  Start the dev server:
    ```bash
    npm start
    ```
    -   App: `http://localhost:3000`

---

## 2. Production Deployment (End-to-End with Docker)

This method deploys both Backend and Frontend on a single server (VPS) using Docker Compose and Nginx.

### Step 1: Create Frontend Dockerfile

Create a file named `Dockerfile` in the `frontend/` directory to build the React app and serve it with Nginx.

**`frontend/Dockerfile`**
```dockerfile
# Stage 1: Build
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
# React Router support (fallback to index.html)
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Step 2: Create Production Docker Compose

Create a new file `docker-compose.prod.yml` in the root directory. This configures the backend, database, and frontend.

**`docker-compose.prod.yml`**
```yaml
services:
  # Backend API
  backend:
    build: .
    restart: always
    environment:
      - ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/jobflowai
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
      # Update allowed origins for production
      - ALLOWED_ORIGINS=http://your-domain.com,http://localhost
    depends_on:
      db:
        condition: service_healthy

  # Database
  db:
    image: postgres:13
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=jobflowai
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d jobflowai"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Frontend (Nginx)
  frontend:
    build: ./frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Step 3: Deploy to VPS

1.  **Provision a Server**: Get a VPS (Ubuntu recommended) from a provider like DigitalOcean, AWS, or Linode.
2.  **Install Docker**: Follow official instructions to install Docker Engine and Docker Compose.
3.  **Clone Repository**:
    ```bash
    git clone https://github.com/your-username/Jobflowai.git
    cd Jobflowai
    ```
4.  **Set Environment Variables**:
    Create a `.env` file in the root directory with production secrets:
    ```bash
    OPENAI_API_KEY=sk-...
    SECRET_KEY=extremely_secure_random_string
    STRIPE_SECRET_KEY=sk_test_...
    ```
    *Note: For the frontend to access the backend, you might need to configure Nginx to proxy `/api` calls to the backend container, or expose the backend on a different port/domain.*

    **Enhanced Production Nginx (Optional but Recommended)**:
    If deploying fully, you usually want Nginx to handle both frontend static files AND proxy API requests to avoid CORS and port issues. You can update the `frontend` service to act as the main gateway:

    Update `frontend/Dockerfile` Nginx config section to:
    ```nginx
    server {
        listen 80;
        
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```

5.  **Run Deployment**:
    ```bash
    docker-compose -f docker-compose.prod.yml up -d --build
    ```

6.  **Verify**:
    -   Visit `http://your-server-ip`.
    -   The frontend should load and be able to communicate with the backend via `/api/`.

---

## 3. Alternative: Cloud Deployment (Vercel + Render)

**Frontend (Vercel)**:
1.  Push code to GitHub.
2.  Import project in Vercel.
3.  Set Root Directory to `frontend`.
4.  Add Environment Variable: `REACT_APP_API_BASE_URL` = `https://your-backend-url.com/api/v1`.

**Backend (Render/Railway)**:
1.  Connect GitHub repo.
2.  Select `Dockerfile` (root path).
3.  Set Environment Variables (`DATABASE_URL`, `OPENAI_API_KEY`).
4.  The service will provision a PostgreSQL DB (or you add one) and run the backend.
