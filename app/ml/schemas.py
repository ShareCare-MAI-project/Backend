from pydantic import BaseModel

from app.items.enums import ItemCategory


class AnalysisResponse(BaseModel):
    name: str
    description: str
    category: ItemCategory
