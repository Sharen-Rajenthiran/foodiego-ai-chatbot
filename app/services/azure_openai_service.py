import os
from typing import List, Optional
from openai import AzureOpenAI
from app.config import settings
from app.models import ChatMessage


class AzureOpenAIService:
    """Service for interacting with Azure OpenAI."""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.openai_api_key,
            api_version=settings.openai_api_version,
            azure_endpoint=settings.openai_endpoint
        )
        self.deployment_name = settings.azure_openai_deployment_name
        
        # System prompt for the food chatbot
        self.system_prompt = """You are a helpful AI assistant for FoodieGo, a food delivery and restaurant discovery platform. 
        Your role is to help customers understand what restaurants, cities, and menu items are available.

        Available cities: New York, San Francisco, Chicago, Austin, Seattle, Boston, Denver, Los Angeles, Portland, Miami

        Available restaurants: The Golden Plate, Saffron Kitchen, Blue Moon Bistro, Rustic Table, Spice Garden, 
        Coastal Catch, Urban Farmhouse, Mountain View Grill, Sunset Terrace, Heritage Kitchen

        Available cuisines: Italian, Japanese, Mexican, Chinese, American, French, Thai, Indian, Korean, Spanish

        Example menu items: Burgers, Pasta, Pizza, Sushi, Ice cream

        Guidelines:
        - Be friendly and helpful
        - Provide accurate information about available restaurants, cities, and menu items
        - If asked about something not in the available options, politely explain what is available
        - Help customers find restaurants by cuisine, location, or specific menu items
        - Keep responses concise but informative
        - Always maintain a positive and professional tone"""

    async def get_chat_response(
        self, 
        user_message: str, 
        conversation_history: Optional[List[ChatMessage]] = None
    ) -> str:
        """
        Get a response from Azure OpenAI based on user message and conversation history.
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            
        Returns:
            The AI assistant's response
        """
        try:
            # Prepare messages for the API
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
