"""FastAPI application entry point"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from zalobot.database import init_db
from zalobot.routers import webhook, payment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager - handles startup and shutdown events
    """
    # Startup
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")
    
    yield  # App runs here
    
    # Shutdown 
    logger.info("Shutting down...")


# Create FastAPI app with lifespan
app = FastAPI(
    title="ZaloBot Pro",
    description="System for selling digital products on Zalo",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(webhook.router)
app.include_router(payment.router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ZaloBot Pro API",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/zalo_verifierIyIx3Axv7nXLYQmYXunzU7w4qaQIyWOSCpKn.html")
async def verify_domain():
    file_path = "zalo_verifierIyIx3Axv7nXLYQmYXunzU7w4qaQIyWOSCpKn.html"
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
