from pydantic import BaseModel

class AnalysisResponse(BaseModel):
    name: str
    description: str
    category: str
