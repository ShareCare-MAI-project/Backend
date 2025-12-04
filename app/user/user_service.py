from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from app.auth.utils.otp_manager import OTPManager
from app.user.user_base import UserBase
from app.user.user_schemas import UserFullInfoResponse
from app.auth.utils.phone_number import PhoneNumber
from app.utils.consts import SUCCESS_RESPONSE


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

    @staticmethod
    async def update_verification(db: AsyncSession, user: UserBase, verified: bool, organization_name: str | None):
        user.is_verified = verified
        user.organization_name = organization_name
        await db.merge(user)
        await db.commit()
        await db.refresh(user)
        return SUCCESS_RESPONSE
