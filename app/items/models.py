import uuid
from datetime import datetime, UTC
from typing import Optional

import uuid_utils
from sqlalchemy import String, Text, Enum, ForeignKey, DateTime, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.items.enums import ItemCategory, ItemStatus, ItemDelivery


class ItemBase(Base):
    __tablename__ = "items"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid_utils.uuid7)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipient_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"),
                                                              nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String)
    # latitude = Column(String)
    # longitude = Column(String)
    category: Mapped[ItemCategory] = mapped_column(Enum(ItemCategory, name="item_category"))
    status: Mapped[ItemStatus] = mapped_column(Enum(ItemStatus, name="item_status"), nullable=False,
                                               default=ItemStatus.listed)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    image_bases: Mapped[list['ItemImageBase']] = relationship(
        "ItemImageBase",
        cascade="all, delete-orphan"
    )

    delivery_bases: Mapped[list['ItemDeliveryTypeBase']] = relationship(
        "ItemDeliveryTypeBase",
        cascade="all, delete-orphan"
    )


class ItemDeliveryTypeBase(Base):
    __tablename__ = "items_delivery_types"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("items.id", ondelete="CASCADE"))
    delivery_type: Mapped[ItemDelivery] = mapped_column(Enum(ItemDelivery, name="item_delivery_type"))


class ItemImageBase(Base):
    __tablename__ = "items_images"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("items.id", ondelete="CASCADE"))
    image: Mapped[str] = mapped_column(String)  # Путь или ссылка
