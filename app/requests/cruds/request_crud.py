from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql._typing import _ColumnExpressionArgument

from app.requests.models import RequestBase


class RequestCrud:
    @staticmethod
    async def create_request(db: AsyncSession, request: RequestBase):
        db.add(request)

    @staticmethod
    async def get_filtered_requests(db: AsyncSession, *whereclause: _ColumnExpressionArgument[bool]) -> list[RequestBase]:
        stmt = select(RequestBase).where(*whereclause).options(
            selectinload(RequestBase.delivery_bases)
        )
        return list((await db.scalars(stmt)).all())
