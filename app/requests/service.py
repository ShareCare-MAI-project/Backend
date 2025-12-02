import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.requests.schemas import Request
from app.requests.mappers import Requests_to_RequestBase
from app.utils.consts import SUCCESS_RESPONSE
from app.requests.cruds.request_crud import RequestCrud
from app.requests.cruds.request_delivery_crud import RequestDeliveryCrud
from app.requests.mappers import RequestDelivery_to_RequestDeliveryTypeBase
from app.items.cruds.item_crud import ItemCrud
from app.requests.schemas import RequestWithId


class RequestService:
    @staticmethod
    async def create_reqeust(db: AsyncSession, request: Request, user_id: uuid.UUID):
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

    @staticmethod
    async def edit_request(db: AsyncSession, request: RequestWithId, user_id: uuid.UUID):
        request_base = await RequestCrud.get_request(db, request_id=request.id)

        if user_id != request_base.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав")

        # is there better way?
        request_base.category = request.category
        request_base.text = request.text
        request_base.location = request.location

        await db.merge(request_base)

        await RequestDeliveryCrud.delete(db, request_id=request.id)
        await db.flush()

        to_await = []
        for delivery_type in request.delivery_types:
            job = RequestDeliveryCrud.create(db, RequestDelivery_to_RequestDeliveryTypeBase(delivery=delivery_type,
                                                                                            request_id=request.id))
            to_await.append(job)

        for i in to_await:
            await i

        await db.commit()
        await db.refresh(request_base)
        return SUCCESS_RESPONSE

    @staticmethod
    async def delete_request(db: AsyncSession, request_id: uuid.UUID, user_id: uuid.UUID):

        request_base = await RequestCrud.get_request(db, request_id=request_id)

        if user_id != request_base.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав")

        await db.delete(request_base)
        await db.commit()
