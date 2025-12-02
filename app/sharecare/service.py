import uuid

from sqlalchemy import or_, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.items.cruds.item_crud import ItemCrud
from app.items.enums import ItemStatus
from app.items.mappers import ItemBase_to_ItemResponse
from app.items.mappers import ItemBase_to_ItemTelegramResponse
from app.items.models import ItemBase
from app.sharecare.schemas import ShareCareItemsResponse
from app.utils.funcs.get_user_telegram import get_user_telegram
from app.common.schemas import SearchRequest
from app.requests.models import RequestDeliveryTypeBase, RequestBase
from app.requests.schemas import RequestResponse
from app.utils.funcs.search_init_statement import search_init_statement
from app.requests.mappers import request_bases_to_request_responses


class ShareCareService:
    @staticmethod
    async def get_sharecare_items(db: AsyncSession, user_id: uuid.UUID) -> ShareCareItemsResponse:
        responses = ItemCrud.get_filtered_items(db,
                                                (ItemBase.status == ItemStatus.chosen), (ItemBase.owner_id == user_id)
                                                )

        my_published_items = ItemCrud.get_filtered_items(db,
                                                         (ItemBase.status == ItemStatus.listed),
                                                         (ItemBase.owner_id == user_id)
                                                         )

        return ShareCareItemsResponse(
            responses=[ItemBase_to_ItemTelegramResponse(
                telegram=await get_user_telegram(db, response.recipient_id),
                item=response
            ) for response in await responses],
            my_published_items=list(map(ItemBase_to_ItemResponse, await my_published_items)),
        )

    @staticmethod
    async def search_requests(
            db: AsyncSession,
            request: SearchRequest,
            user_id: uuid.UUID,
            organization_name: str | None
    ) -> list[RequestResponse]:
        # https://habr.com/ru/companies/beeline_cloud/articles/742214/?ysclid=milavy3vv3200505062
        stmt = search_init_statement(base=RequestBase, delivery_base=RequestDeliveryTypeBase, category=request.category,
                                     delivery_types=request.delivery_types)
        query = request.query
        stmt = stmt.where(
            RequestBase.user_id != user_id
        )
        if query and query.strip():
            stmt = stmt.where(
                func.similarity(RequestBase.text, query) > 0.1
            ).order_by(
                func.similarity(RequestBase.text, query).desc()
            )
        else:
            stmt = stmt.order_by(RequestBase.edited_at.desc())

        stmt = stmt.offset(request.offset).limit(request.to_load)

        result = await db.scalars(stmt)
        return request_bases_to_request_responses(list(result.all()), organization_name=organization_name)
