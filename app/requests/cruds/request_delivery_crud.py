from sqlalchemy.ext.asyncio import AsyncSession

from app.items.models import ItemDeliveryTypeBase
from app.requests.models import RequestDeliveryTypeBase


class RequestDeliveryCrud:
    @staticmethod
    async def create(db: AsyncSession, request_delivery: RequestDeliveryTypeBase):
        db.add(request_delivery)
