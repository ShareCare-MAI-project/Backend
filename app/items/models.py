import uuid
import enum
from sqlalchemy import Column, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(enum.Enum):
    clothes = "Одежда"
    toys = "Игрушки"
    home = "Быт"
    electronics = "Электроника"
    other = "Другое"

class Status(enum.Enum):
    listed = "выложено"
    chosen = "выбран получатель"
    closed = "закрыто"

class Delivery(enum.Enum):
    pickup = "Самовывоз"
    post = "Доставка почтой"
    owner_delivery = "Человек готов доставить сам"

class Item(Base):
    __tablename__ = "items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner = Column(UUID(as_uuid=True), nullable=False)
    recipient = Column(UUID(as_uuid=True), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    category = Column(Enum(Category))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    edited_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(Enum(Status), nullable=False, default=Status.listed)

class ItemDeliveryType(Base):
    __tablename__ = "items_delivery_types"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    delivery_type = Column(Enum(Delivery))

class ItemImage(Base):
    __tablename__ = "items_images"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    image = Column(String)  # путь или ссылка
