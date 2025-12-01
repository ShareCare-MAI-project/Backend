from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils.otp_manager import OTPManager
from app.user.user_base import UserBase
from app.user.user_schemas import UserFullInfoResponse
from app.auth.utils.phone_number import PhoneNumber
from app.items.models import ItemBase


class UserService:
    @staticmethod
    async def get_user_full_info(user: UserBase):
        if user.name is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Пользователь не зарегистрирован"
            )
        return UserFullInfoResponse(
            phone=PhoneNumber(OTPManager.decrypt_phone_number(user.encrypted_phone)),
            name=user.name,
            telegram_username=user.telegram_username,
            is_verified=user.is_verified,
            organization_name=user.organization_name
        )
    
    async def get_QuickInfo(self, user_id: UUID, session: AsyncSession) -> dict:
        user = await UserBase.get_by_id(user_id, session)
    
        if not user:
            raise ValueError(f"Пользователь {user_id} не найден")
    
         # Сколько получено (где user = recipient в ItemBase)
        received = await session.scalar(
            select(func.count(ItemBase.id))
            .where(ItemBase.recipient_id == user_id)
        )
    
        # Сколько отдано (где user = owner в ItemBase)
        donated = await session.scalar(
            select(func.count(ItemBase.id))
            .where(ItemBase.owner_id == user_id)
        )
    
        return {
            "name": user.name or "Без имени",
            "is_verified": user.is_verified,
            "items_received": received or 0,
            "items_donated": donated or 0,
        }
