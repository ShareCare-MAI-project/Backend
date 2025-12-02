import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.items.cruds.item_crud import ItemCrud
from app.items.enums import ItemStatus
from app.items.mappers import ItemBase_to_ItemResponse
from app.items.mappers import ItemBase_to_ItemTelegramResponse
from app.items.models import ItemBase
from app.sharecare.schemas import ShareCareItemsResponse
from app.utils.funcs.get_user_telegram import get_user_telegram


class ShareCareService:
    @staticmethod
    async def get_sharecare_items(db: AsyncSession, user_id: uuid.UUID) -> ShareCareItemsResponse:
        responses = ItemCrud.get_filtered_items(db,
                (ItemBase.status == ItemStatus.chosen),  (ItemBase.owner_id == user_id)
        )

        my_published_items = ItemCrud.get_filtered_items(db,
                (ItemBase.status == ItemStatus.listed), (ItemBase.owner_id == user_id)
        )

        return ShareCareItemsResponse(
            responses=[ItemBase_to_ItemTelegramResponse(
                telegram=await get_user_telegram(db, response.recipient_id),
                item=response
            ) for response in await responses],
            my_published_items=list(map(ItemBase_to_ItemResponse, await my_published_items)),
        )
