"""
Tamil Nadu Real Estate AI Assistant - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import router as api_router
from app.auth_routes import router as auth_router

app = FastAPI(
    title=settings.app_name,
    description="Domain-restricted AI assistant for Tamil Nadu real estate queries",
    version="1.0.0",
    debug=settings.debug
)

# ✅ CORRECT CORS CONFIG (NO OPTIONS HANDLER NEEDED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://purity-prop-f.vercel.app",
        "https://purity-prop-f-git-main-naveens-projects-36f95ce0.vercel.app"
    ],
    allow_credentials=False,  # 🔴 MUST BE FALSE (JWT via headers)
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers (DO NOT add extra prefix)
app.include_router(auth_router)   # /api/auth/...
app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "message": "Tamil Nadu Real Estate AI Assistant API",
        "status": "active"
    }
