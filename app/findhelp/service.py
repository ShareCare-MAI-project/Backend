import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.findhelp.schemas import FindHelpBasicResponse
from app.items.cruds.item_crud import ItemCrud
from app.items.enums import ItemStatus
from app.items.models import ItemBase
from app.requests.cruds.request_crud import RequestCrud
from app.requests.models import RequestBase
from app.items.mappers import ItemBase_to_ItemTelegramResponse
from app.utils.funcs.get_user_telegram import get_user_telegram
from app.requests.mappers import RequestBase_to_RequestResponse
from app.utils.funcs.get_organization_name import get_organization_name


class FindHelpService:
    @staticmethod
    async def get_findhelp_basic_items(db: AsyncSession, user_id: uuid.UUID) -> FindHelpBasicResponse:
        ready_to_help = ItemCrud.get_filtered_items(db, where=(
                ItemBase.status == ItemStatus.chosen and ItemBase.recipient_id == user_id
        ))

        my_requests = RequestCrud.get_filtered_requests(db, where=(
                RequestBase.status == ItemStatus.listed and RequestBase.user_id == user_id
        ))

        organization_name = await get_organization_name(db, user_id)

        return FindHelpBasicResponse(
            ready_to_help=[ItemBase_to_ItemTelegramResponse(
                telegram=await get_user_telegram(db, response.recipient_id),
                item=response
            ) for response in await ready_to_help],
            my_requests=[RequestBase_to_RequestResponse(request, organization_name=organization_name) for request in
                         await my_requests]
        )
