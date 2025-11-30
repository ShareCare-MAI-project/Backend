import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.user.user_base import UserBase


async def get_organization_name(db: AsyncSession, user_id: uuid.UUID) -> str | None:
    return (await UserBase.get_by_id(user_id=user_id, session=db)).organization_name
