import uuid

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.items.models import ItemDeliveryTypeBase


class ItemDeliveryCrud:
    @staticmethod
    async def create(db: AsyncSession, item_delivery: ItemDeliveryTypeBase):
        db.add(item_delivery)

    @staticmethod
    async def delete(db: AsyncSession, item_id: uuid.UUID):
        stmt = delete(ItemDeliveryTypeBase).where(ItemDeliveryTypeBase.item_id == item_id)
        await db.execute(stmt)