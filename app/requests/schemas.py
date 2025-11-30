from pydantic import BaseModel, UUID7

from app.items.enums import ItemCategory, ItemDelivery


class Request(BaseModel):
    text: str
    location: str
    # latitude: Optional[str]
    # longitude: Optional[str]
    category: ItemCategory
    delivery_types: list[ItemDelivery]


class RequestResponse(Request):
    id: UUID7
    user_id: UUID7
    organization_name: str | None
