import uuid
from typing import Optional, List

from sqlalchemy import select, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, Mapped

from app.items.models import ItemBase


class ItemCrud:
    @staticmethod
    async def create_item(db: AsyncSession, item: ItemBase):
        db.add(item)

    @staticmethod
    async def get_item(db: AsyncSession, item_id: uuid.UUID) -> Optional[ItemBase]:
        stmt = select(ItemBase).where(ItemBase.id == item_id).options(
            selectinload(ItemBase.image_bases),
            selectinload(ItemBase.item_delivery_bases)
        )
        return (await db.scalars(stmt)).one_or_none()

    @staticmethod
    async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ItemBase]:
        stmt = select(ItemBase).offset(skip).limit(limit).options(
            selectinload(ItemBase.image_bases),
            selectinload(ItemBase.item_delivery_bases)
        )
        return list((await db.scalars(stmt)).all())

    @staticmethod
    async def get_filtered_items(db: AsyncSession, where: ColumnElement[bool]) -> List[ItemBase]:
        stmt = select(ItemBase).where(where).options(
            selectinload(ItemBase.image_bases),
            selectinload(ItemBase.item_delivery_bases)
        ).order_by(
            ItemBase.edited_at.desc()
        )

        return list((await db.scalars(stmt)).all())

    # @staticmethod
    # async def update_item(db: AsyncSession, item_id: UUID, item: ItemBase) -> Optional[ItemBase]:
    #     pass
    #     # db_item = get_item(db, item_id)
    #     # if not db_item:
    #     #     return None
    #     #
    #     # update_data = item_update.model_dump(exclude_unset=True)
    #     # for key, value in update_data.items():
    #     #     setattr(db_item, key, value)
    #     #
    #     # db.commit()
    #     # db.refresh(db_item)
    #     # return db_item
    #
    # @staticmethod
    # async def delete_item(db: AsyncSession, item_id: UUID) -> bool:
    #     db_item = ItemCrud.get_item(db, item_id)
    #     if not db_item:
    #         return False
    #
    #     await db.delete(db_item)
    #     await db.commit()
    #     return True

    # async def reserve_item(db: AsyncSession, item_id: UUID, recipient_id: UUID):
    #     db_item = get_item(db, item_id)
    #     if not db_item:
    #         return None
    #
    #     db_item.recipient = recipient_id
    #     db_item.status = "выбран получатель"
    #     db.commit()
    #     db.refresh(db_item)
    #     return db_item

    # async def close_item(db: AsyncSession, item_id: UUID):
    #     db_item = get_item(db, item_id)
    #     if not db_item:
    #         return None
    #
    #     db_item.status = ItemStatus.closed
    #     await db.commit()
    #     await db.refresh(db_item)
