import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.requests.schemas import Request
from app.requests.mappers import Requests_to_RequestBase
from app.utils.consts import SUCCESS_RESPONSE
from app.requests.cruds.request_crud import RequestCrud
from app.requests.cruds.request_delivery_crud import RequestDeliveryCrud
from app.requests.mappers import RequestDelivery_to_RequestDeliveryTypeBase


class RequestService:
    @staticmethod
    async def create_item(db: AsyncSession, request: Request, user_id: uuid.UUID):
        request_base = Requests_to_RequestBase(request=request, user_id=user_id)

        await RequestCrud.create_request(db, request_base)
        await db.flush()
        request_id = request_base.id

        to_await = []
        for delivery_type in request.delivery_types:
            job = RequestDeliveryCrud.create(db, RequestDelivery_to_RequestDeliveryTypeBase(delivery=delivery_type,
                                                                                            request_id=request_id))
            to_await.append(job)

        for i in to_await:
            await i

        await db.commit()
        await db.refresh(request_base)

        return SUCCESS_RESPONSE
