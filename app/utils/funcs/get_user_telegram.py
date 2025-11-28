import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.user.user_base import UserBase


async def get_user_telegram(db: AsyncSession, user_id: uuid.UUID) -> str:
    return (await UserBase.get_by_id(user_id=user_id, session=db)).telegram_username