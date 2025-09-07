import os
from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Azure OpenAI Configuration - support multiple naming conventions
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_version: str = "2024-02-15-preview"
    azure_openai_deployment_name: str = "gpt-4"
    
    # Alternative naming for existing environment variables
    api_key: Optional[str] = None
    azure_endpoint: Optional[str] = None
    api_version: Optional[str] = None
    
    # Server Configuration
    host: str = "localhost"
    port: int = 8001
    debug: bool = False
    
    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields
    
    @property
    def openai_api_key(self) -> str:
        """Get the OpenAI API key from either naming convention."""
        return self.azure_openai_api_key or self.api_key or ""
    
    @property
    def openai_endpoint(self) -> str:
        """Get the OpenAI endpoint from either naming convention."""
        return self.azure_openai_endpoint or self.azure_endpoint or ""
    
    @property
    def openai_api_version(self) -> str:
        """Get the OpenAI API version from either naming convention."""
        return self.azure_openai_api_version or self.api_version or "2024-02-15-preview"
    
    def validate_azure_openai_config(self) -> bool:
        """Validate that Azure OpenAI configuration is complete."""
        return bool(self.openai_api_key and self.openai_endpoint)


# Global settings instance
settings = Settings()

# Validate configuration on startup
if not settings.validate_azure_openai_config():
    print("Warning: Azure OpenAI configuration is incomplete.")
    print("Please set the following environment variables:")
    print("- AZURE_OPENAI_API_KEY (or API_KEY)")
    print("- AZURE_OPENAI_ENDPOINT (or AZURE_ENDPOINT)")
    print("The server will start but chat functionality may not work.")
