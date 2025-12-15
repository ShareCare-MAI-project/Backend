from pydantic_settings import BaseSettings
import os


class MLConfig(BaseSettings):
    # API ключ для OpenRouter
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    MODEL_NAME: str = "openai/gpt-5-mini"
    
    
    class Config:
        env_file = ".env"


ml_config = MLConfig()
