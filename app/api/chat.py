from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse
from app.services.azure_openai_service import AzureOpenAIService
from app.logging_config import logger

router = APIRouter()
azure_openai_service = AzureOpenAIService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for interacting with the AI assistant.
    
    Args:
        request: Chat request containing message and optional conversation history
        
    Returns:
        Chat response from the AI assistant
    """
    logger.info(f"Chat request received: {request.message[:100]}...")
    
    try:
        if not request.message.strip():
            logger.warning("Empty message received")
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Log conversation history length
        history_length = len(request.conversation_history) if request.conversation_history else 0
        logger.info(f"Processing chat with {history_length} previous messages")
        
        # Get response from Azure OpenAI
        response = await azure_openai_service.get_chat_response(
            user_message=request.message,
            conversation_history=request.conversation_history
        )
        
        logger.info(f"Chat response generated successfully: {response[:100]}...")
        
        return ChatResponse(
            response=response,
            conversation_id=None  # Could be implemented for session management
        )
        
    except HTTPException as e:
        logger.error(f"HTTP exception in chat endpoint: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status of the service
    """
    logger.info("API health check endpoint accessed")
    return {"status": "healthy", "message": "AI Chatbot service is running"}
