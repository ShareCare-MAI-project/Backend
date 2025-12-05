import uuid

from pydantic import BaseModel

from app.items.enums import ItemCategory, ItemDelivery, ItemStatus


class SearchRequest(BaseModel):
    query: str
    category: ItemCategory | None
    delivery_types: list[ItemDelivery]
    offset: int
    to_load: int


class ItemQuickInfoResponse(BaseModel):
    status: ItemStatus
    opponent_id: uuid.UUID
    opponent_name: str
    opponent_is_verified: bool
    opponent_organization_name: str | None
    opponent_donated: int
    opponent_received: int
