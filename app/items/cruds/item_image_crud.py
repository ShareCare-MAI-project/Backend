from sqlalchemy.ext.asyncio import AsyncSession

from app.items.models import ItemImageBase


class ItemImageCrud:
    @staticmethod
    async def create(db: AsyncSession, item_image: ItemImageBase):
        db.add(item_image)
