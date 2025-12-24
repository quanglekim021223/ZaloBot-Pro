"""Entry point - Import and run the FastAPI app"""
from zalobot.main import app

# This allows running: uvicorn main:app --reload
__all__ = ["app"]

