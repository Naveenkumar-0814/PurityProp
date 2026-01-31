"""
Tamil Nadu Real Estate AI Assistant - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import router
from app.auth_routes import router as auth_router


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Domain-restricted AI assistant for Tamil Nadu real estate queries",
    version="1.0.0",
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(router)





@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Tamil Nadu Real Estate AI Assistant API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )


