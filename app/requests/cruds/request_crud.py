from sqlalchemy import ColumnElement, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.requests.models import RequestBase


class RequestCrud:
    @staticmethod
    async def create_request(db: AsyncSession, request: RequestBase):
        db.add(request)

    @staticmethod
    async def get_filtered_requests(db: AsyncSession, where: ColumnElement[bool]) -> list[RequestBase]:
        stmt = select(RequestBase).where(where).options(
            selectinload(RequestBase.delivery_bases)
        ).order_by(
            RequestBase.edited_at.desc()
        )
        return list((await db.scalars(stmt)).all())
