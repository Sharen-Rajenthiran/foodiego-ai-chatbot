#!/usr/bin/env python3
"""
Main entry point for the FoodieGo AI Chatbot API.
Run this file to start the FastAPI server.
"""

import uvicorn
from app.config import settings
from app.logging_config import logger

if __name__ == "__main__":
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    logger.info(f"Debug mode: {settings.debug}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
