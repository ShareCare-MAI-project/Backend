from sqlalchemy.ext.asyncio import AsyncSession

from app.requests.models import RequestBase


class RequestCrud:
    @staticmethod
    async def create_request(db: AsyncSession, request: RequestBase):
        db.add(request)
