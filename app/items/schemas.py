from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
import enum

class Category(str, enum.Enum):
    clothes = "Одежда"
    toys = "Игрушки"
    home = "Быт"
    electronics = "Электроника"
    other = "Другое"

class Status(str, enum.Enum):
    listed = "выложено"
    chosen = "выбран получатель"
    closed = "закрыто"

class Delivery(str, enum.Enum):
    pickup = "Самовывоз"
    post = "Доставка почтой"
    owner_delivery = "Человек готов доставить сам"

class ItemBase(BaseModel):
    title: str
    description: Optional[str]
    location: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    category: Optional[Category]
    status: Status = Status.listed

class ItemCreate(ItemBase):
    owner: UUID

class ItemResponse(ItemBase):
    id: UUID
    owner: UUID
    recipient: Optional[UUID] = None
    created_at: datetime
    edited_at: Optional[datetime] = None

class ItemOut(ItemBase):
    id: UUID
    owner: UUID
    recipient: Optional[UUID]
    created_at: datetime
    edited_at: Optional[datetime]
    class Config:
        orm_mode = True

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    category: Optional[Category] = None
    status: Optional[Status] = None
    recipient: Optional[UUID] = None