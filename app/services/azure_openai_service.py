import os
from typing import List, Optional
from openai import AzureOpenAI
from app.config import settings
from app.models import ChatMessage
from app.logging_config import logger


class AzureOpenAIService:
    """Service for interacting with Azure OpenAI."""
    
    def __init__(self):
        logger.info("Initializing Azure OpenAI service")
        logger.info(f"Using deployment: {settings.deployment_name}")
        logger.info(f"Using API version: {settings.api_version}")
        
        self.client = AzureOpenAI(
            api_key=settings.api_key,
            api_version=settings.api_version,
            azure_endpoint=settings.azure_endpoint
        )
        
        self.deployment_name = settings.deployment_name
        
        logger.info("Azure OpenAI service initialized successfully")
        
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
        logger.info(f"Generating chat response for message: {user_message[:50]}...")
        
        try:
            # Prepare messages for the API
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                logger.info(f"Adding {len(conversation_history)} messages from conversation history")
                for msg in conversation_history:
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            logger.info(f"Sending request to Azure OpenAI with {len(messages)} total messages")
            
            # Call Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                top_p=0.9
            )
            
            response_content = response.choices[0].message.content.strip()
            logger.info(f"Successfully received response from Azure OpenAI: {response_content[:100]}...")
            
            return response_content
            
        except Exception as e:
            logger.error(f"Error in Azure OpenAI service: {str(e)}", exc_info=True)
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
