#!/usr/bin/env python3
"""
Main entry point for the FoodieGo AI Chatbot API.
Run this file to start the FastAPI server.
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
