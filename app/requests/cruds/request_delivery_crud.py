import uuid

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.items.models import ItemDeliveryTypeBase
from app.requests.models import RequestDeliveryTypeBase


class RequestDeliveryCrud:
    @staticmethod
    async def create(db: AsyncSession, request_delivery: RequestDeliveryTypeBase):
        db.add(request_delivery)

    @staticmethod
    async def delete(db: AsyncSession, request_id: uuid.UUID):
        stmt = delete(RequestDeliveryTypeBase).where(RequestDeliveryTypeBase.request_id == request_id)
        await db.execute(stmt)

