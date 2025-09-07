from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse
from app.services.azure_openai_service import AzureOpenAIService

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
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get response from Azure OpenAI
        response = await azure_openai_service.get_chat_response(
            user_message=request.message,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(
            response=response,
            conversation_id=None  # Could be implemented for session management
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status of the service
    """
    return {"status": "healthy", "message": "AI Chatbot service is running"}
