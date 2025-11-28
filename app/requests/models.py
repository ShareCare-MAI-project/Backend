import uuid
from datetime import datetime, UTC
from typing import Optional

import uuid_utils
from sqlalchemy import String, Text, Enum, ForeignKey, DateTime, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.items.enums import ItemCategory, ItemStatus, ItemDelivery


class RequestBase(Base):
    __tablename__ = "requests"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid_utils.uuid7)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(String)
    category: Mapped[ItemCategory] = mapped_column(Enum(ItemCategory, name="request_category"))
    status: Mapped[ItemStatus] = mapped_column(Enum(ItemStatus, name="request_status"), nullable=False,
                                               default=ItemStatus.listed)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC),
                                                          onupdate=lambda: datetime.now(UTC))

    request_delivery_bases: Mapped[list['RequestDeliveryTypeBase']] = relationship(
        "RequestDeliveryTypeBase",
        cascade="all, delete-orphan"
    )


class RequestDeliveryTypeBase(Base):
    __tablename__ = "request_delivery_types"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    request_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("requests.id", ondelete="CASCADE"))
    delivery_type: Mapped[ItemDelivery] = mapped_column(Enum(ItemDelivery, name="request_delivery_type"))
