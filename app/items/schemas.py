from typing import Optional

from pydantic import BaseModel, UUID7

from app.items.enums import ItemCategory, ItemDelivery


class Item(BaseModel):
    title: str
    description: str
    location: str
    # latitude: Optional[str]
    # longitude: Optional[str]
    category: ItemCategory
    delivery_types: list[ItemDelivery]


class ItemResponse(Item):
    id: UUID7
    owner: UUID7
    recipient: Optional[UUID7] = None
    images: list[str]


class ItemTelegramResponse(ItemResponse):
    telegram: str
