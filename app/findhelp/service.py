import uuid

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.common.schemas import SearchRequest
from app.findhelp.schemas import FindHelpBasicResponse
from app.items.cruds.item_crud import ItemCrud
from app.items.enums import ItemStatus
from app.items.mappers import ItemBase_to_ItemTelegramResponse, item_bases_to_item_responses
from app.items.models import ItemBase, ItemDeliveryTypeBase
from app.requests.cruds.request_crud import RequestCrud
from app.requests.mappers import RequestBase_to_RequestResponse
from app.requests.models import RequestBase
from app.utils.funcs.get_organization_name import get_organization_name
from app.utils.funcs.get_user_telegram import get_user_telegram
from app.utils.funcs.search_init_statement import search_init_statement
from app.items.schemas import ItemResponse
from app.findhelp.schemas import TakeItemResponse


class FindHelpService:
    @staticmethod
    async def take_item(db: AsyncSession, user_id: uuid.UUID, item_id: uuid.UUID) -> TakeItemResponse:
        item = await ItemCrud.get_item(db, item_id)
        if item.status == ItemStatus.listed:
            item.status = ItemStatus.chosen
            item.recipient_id = user_id

            telegram = get_user_telegram(db, item.owner_id)
            await ItemCrud.update_item(db, new_item=item)
            await db.flush(item)
            await db.commit()
            return TakeItemResponse(telegram=await telegram)
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Предмет уже взяли 0_о")

    @staticmethod
    async def get_findhelp_basic_items(db: AsyncSession, user_id: uuid.UUID) -> FindHelpBasicResponse:
        ready_to_help = ItemCrud.get_filtered_items(db, (
                (ItemBase.status == ItemStatus.chosen) & (ItemBase.recipient_id == user_id)
        ))

        my_requests = RequestCrud.get_filtered_requests(db, (
                (RequestBase.status == ItemStatus.listed) & (RequestBase.user_id == user_id)
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

    @staticmethod
    async def search_items(
            db: AsyncSession,
            request: SearchRequest
    ) -> list[ItemResponse]:
        # https://habr.com/ru/companies/beeline_cloud/articles/742214/?ysclid=milavy3vv3200505062
        stmt = search_init_statement(base=ItemBase, delivery_base=ItemDeliveryTypeBase, category=request.category,
                                     delivery_types=request.delivery_types)
        query = request.query
        if query and query.strip():
            stmt = stmt.where(
                or_(
                    func.similarity(ItemBase.title, query) > 0.1,
                    func.similarity(ItemBase.description, query) > 0.1
                )
            ).order_by(
                (
                        func.similarity(ItemBase.title, query) * 2 +
                        func.similarity(ItemBase.description, query) * 1
                ).desc()
            )
        else:
            stmt = stmt.order_by(ItemBase.edited_at.desc())

        stmt = stmt.offset(request.offset).limit(request.to_load)

        result = await db.scalars(stmt)
        return item_bases_to_item_responses(list(result.all()))

        # if query and query.strip():
        #     stmt = stmt.where(
        #         func.similarity(RequestBase.text, query) > 0.1
        #     ).order_by(
        #         func.similarity(RequestBase.text, query).desc()
        #     )
        # else:
        #     stmt = stmt.order_by(RequestBase.edited_at.desc())
