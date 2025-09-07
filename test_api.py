#!/usr/bin/env python3
"""
Simple test script to verify the API is working correctly.
Run this after starting the server to test the endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_health():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_chat():
    """Test the chat endpoint."""
    print("\nTesting chat endpoint...")
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
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_root():
    """Test the root endpoint."""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing FoodieGo AI Chatbot API")
    print("=" * 40)
    
    # Test endpoints
    health_ok = test_health()
    root_ok = test_root()
    chat_ok = test_chat()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"Health endpoint: {'✓' if health_ok else '✗'}")
    print(f"Root endpoint: {'✓' if root_ok else '✗'}")
    print(f"Chat endpoint: {'✓' if chat_ok else '✗'}")
    
    if all([health_ok, root_ok, chat_ok]):
        print("\n🎉 All tests passed! The API is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the server logs.")
