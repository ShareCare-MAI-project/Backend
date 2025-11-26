import uuid
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.items.crud import ItemCrud
from app.items.mappers import ItemBase_to_ItemResponse, Item_to_ItemBase
from app.items.schemas import ItemResponse, Item
from app.utils.consts import SUCCESS_RESPONSE


class ItemsService:
    @staticmethod
    async def get_item(db: AsyncSession, item_id: UUID) -> ItemResponse:
        item = await ItemCrud.get_item(db, item_id)
        delivery_types = list()  # TODO
        images = ["https://i.pinimg.com/736x/73/fa/4a/73fa4ad5af52fe3bd6a3fd682e98f102.jpg",
                  "https://i.pinimg.com/1200x/a9/9d/b3/a99db39699bf64222d2338d61cbca5e6.jpg",
                  "https://i.pinimg.com/736x/9f/8d/b8/9f8db8c29183e66189762020d46f57b9.jpg"]  # TODO

        if not item:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Товар не найден")

        return ItemBase_to_ItemResponse(item, delivery_types=delivery_types, images=images)

    @staticmethod
    async def get_items(db: AsyncSession) -> list[ItemResponse]:
        # Now returns all
        items = await ItemCrud.get_items(db)
        return list(map(
            lambda item: ItemBase_to_ItemResponse(item, [], []),  # TODO
            items
        ))

    @staticmethod
    async def create_item(db: AsyncSession, item: Item, owner_id: uuid.UUID):
        item_base = Item_to_ItemBase(item=item, owner_id=owner_id)
        await ItemCrud.create_item(db, item_base)

        await db.commit()
        await db.refresh(item_base)

        return SUCCESS_RESPONSE
