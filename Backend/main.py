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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "message": "Tamil Nadu Real Estate AI Assistant API",
        "status": "active"
    }
