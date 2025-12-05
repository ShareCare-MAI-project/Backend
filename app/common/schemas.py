from pydantic import BaseModel

from app.items.enums import ItemCategory, ItemDelivery


class SearchRequest(BaseModel):
    query: str
    category: ItemCategory | None
    delivery_types: list[ItemDelivery]
    offset: int
    to_load: int
