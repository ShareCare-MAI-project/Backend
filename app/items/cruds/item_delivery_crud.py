from sqlalchemy.ext.asyncio import AsyncSession

from app.items.models import ItemDeliveryTypeBase


class ItemDeliveryCrud:
    @staticmethod
    async def create(db: AsyncSession, item_delivery: ItemDeliveryTypeBase):
        db.add(item_delivery)
