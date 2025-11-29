from pydantic import BaseModel
from typing import Optional


class AnalysisResponse(BaseModel):
    """Результат анализа фото"""
    name: str  
    description: str  
    category: str  
    error: Optional[str] = None


class AnalysisRequest(BaseModel):
    """Запрос для анализа фото"""
    image_url: str  
