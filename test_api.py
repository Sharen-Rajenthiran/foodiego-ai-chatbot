#!/usr/bin/env python3
"""
Simple test script to verify the API is working correctly.
Run this after starting the server to test the endpoints.
"""

import requests
import json
import logging

# Set up logging for the test script
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8001"

def test_health():
    """Test the health endpoint."""
    logger.info("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        logger.info(f"Status: {response.status_code}")
        logger.info(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

def test_chat():
    """Test the chat endpoint."""
    logger.info("Testing chat endpoint...")
    try:
        payload = {
            "message": "What restaurants are available in New York?",
            "conversation_history": []
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        logger.info(f"Status: {response.status_code}")
        if response.status_code == 200:
            logger.info(f"Response: {response.json()}")
        else:
            logger.error(f"Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

def test_root():
    """Test the root endpoint."""
    logger.info("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        logger.info(f"Status: {response.status_code}")
        logger.info(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

if __name__ == "__main__":
    logger.info("Testing FoodieGo AI Chatbot API")
    logger.info("=" * 40)
    
    # Test endpoints
    health_ok = test_health()
    root_ok = test_root()
    chat_ok = test_chat()
    
    logger.info("=" * 40)
    logger.info("Test Results:")
    logger.info(f"Health endpoint: {'✓' if health_ok else '✗'}")
    logger.info(f"Root endpoint: {'✓' if root_ok else '✗'}")
    logger.info(f"Chat endpoint: {'✓' if chat_ok else '✗'}")
    
    if all([health_ok, root_ok, chat_ok]):
        logger.info(" All tests passed! The API is working correctly.")
    else:
        logger.error(" Some tests failed. Check the server logs.")
