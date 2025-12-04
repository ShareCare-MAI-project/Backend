import uuid

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.items.models import ItemImageBase


class ItemImageCrud:
    @staticmethod
    async def create(db: AsyncSession, item_image: ItemImageBase):
        db.add(item_image)

    @staticmethod
    async def delete(db: AsyncSession, item_id: uuid.UUID):
        stmt = delete(ItemImageBase).where(ItemImageBase.item_id == item_id)
        await db.execute(stmt)
