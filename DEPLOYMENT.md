# JobFlowAI Deployment Guide

## 🚀 Recommended: Cloud Deployment (Vercel + Render)

This project is configured for a seamless cloud deployment using **Render** (Backend & Database) and **Vercel** (Frontend).

### Phase 1: Backend Deployment (Render)

1.  **Sign up/Login** to [Render](https://render.com).
2.  **Create a New Blueprint Instance**:
    *   Go to Dashboard -> "New" -> "Blueprint".
    *   Connect your GitHub repository.
    *   Render will automatically detect `render.yaml` in the root.
3.  **Apply the Blueprint**:
    *   Render will prompt to create a **Database** (`jobflowai-db`) and a **Web Service** (`jobflowai-backend`).
    *   Click "Apply".
4.  **Wait for Build**:
    *   Render will build the Docker image and start the service.
    *   Once "Live", copy the **Backend URL** (e.g., `https://jobflowai-backend.onrender.com`).

**Troubleshooting Env Vars:**
If automatic configuration misses variables, manually add these in the Render Dashboard (Environment):
*   `SECRET_KEY`: (Generate a random string)
*   `OPENAI_API_KEY`: (Your OpenAI Key)
*   `ALLOWED_ORIGINS`: `https://your-frontend.vercel.app` (You will update this after Phase 2)
*   `PORT`: `10000` (Default)

---

### Phase 2: Frontend Deployment (Vercel)

1.  **Sign up/Login** to [Vercel](https://vercel.com).
2.  **Add New Project**:
    *   "Import Project" -> Select your GitHub repository.
3.  **Configure Project**:
    *   **Root Directory**: Click "Edit" and select `frontend`. **(Crucial Step)**.
    *   **Framework Preset**: Create React App (Auto-detected).
    *   **Build Command**: `npm run build`.
4.  **Environment Variables**:
    Add the following variables so the frontend can find the backend:
    *   `REACT_APP_API_BASE_URL`: Paste your Render Backend URL (e.g., `https://jobflowai-backend.onrender.com`).
    *   `REACT_APP_API_BASE`: (Same value as above, for safety).
5.  **Deploy**:
    *   Click "Deploy".
    *   Vercel will build and assign a domain (e.g., `jobflowai.vercel.app`).

---

### Phase 3: Final Connection

1.  Go back to **Render Dashboard** -> `jobflowai-backend` service -> **Environment**.
2.  Update `ALLOWED_ORIGINS`:
    *   Set it to your new Vercel domain (e.g., `https://jobflowai.vercel.app`).
    *   This ensures CORS requests are allowed.
3.  **Done!** Your app is now live.

---

## 💻 Alternative: Local Deployment (Docker)

To run the entire stack locally:

1.  **Configure .env**:
    *   Ensure `backend/.env` exists or `docker-compose.yml` env vars are sufficient.
2.  **Run Docker Compose**:
    ```bash
    docker-compose -f docker-compose.prod.yml up --build
    ```
3.  **Access**:
    *   Frontend: `http://localhost:80`
    *   Backend: `http://localhost:8080` (internal access)

## ⚠️ Important Configuration Notes

*   **Port**: The backend listens on port `8080` by default but respects the `PORT` env var (required for Render).
*   **Database**: The `render.yaml` blueprint creates a managed PostgreSQL instance automatically.
*   **CORS**: Ensure `ALLOWED_ORIGINS` matches the frontend domain exactly (no trailing slash).
