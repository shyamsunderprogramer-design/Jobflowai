import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base
# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Import Routers
from backend.routes.auth import router as auth_router
from backend.routes.auth_reset import router as auth_reset_router
from backend.routes.compare import router as compare_router
from backend.routes.enhance import router as enhance_router
from backend.routes.feedback import router as feedback_router
from backend.routes.generate import router as generate_router
from backend.routes.jobs import router as jobs_router
from backend.routes.jobs_debug import router as jobs_debug_router
from backend.routes.news import router as news_router
from backend.routes.parse import router as parse_router
from backend.routes.payments import router as payments_router
from backend.routes.profile import router as profile_router
from backend.routes.resume_cover import router as resume_cover_router
from backend.routes.resume_routes import router as resume_router
from backend.routes.trial import router as trial_router
# Excluding resume.py as it appears to be legacy/unsecured compared to resume_routes.py

app = FastAPI(title="JobFlowAI Backend")

# Configure CORS
# In production, set ALLOWED_ORIGINS to "https://your-frontend.vercel.app"
origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth_router)
app.include_router(auth_reset_router)
app.include_router(compare_router)
app.include_router(enhance_router)
app.include_router(feedback_router)
app.include_router(generate_router)
app.include_router(jobs_router)
app.include_router(jobs_debug_router)
app.include_router(news_router)
app.include_router(parse_router)
app.include_router(payments_router)
app.include_router(profile_router)
app.include_router(resume_cover_router)
app.include_router(resume_router)
app.include_router(trial_router)

@app.get("/")
def home():
    return {"message": "JobFlowAI Backend is running!", "docs_url": "/docs"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Reload=False for production
    uvicorn.run(app, host="0.0.0.0", port=port)
