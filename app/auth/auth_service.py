import uuid_utils
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from app.auth.auth_schemas import LoginRequest, OTPVerifyRequest, AuthResponse
from app.auth.auth_schemas import UserRegistrationRequest
from app.auth.token_base import TokenBase
from app.auth.utils.otp_manager import OTPManager
from app.user.user_base import UserBase
from app.utils.consts import SUCCESS_RESPONSE

FAKE_OTP = "1111"


class AuthService:

    @staticmethod
    async def request_otp(request: LoginRequest) -> dict:
        """Отправить OTP код на телефон"""
        phone = request.phone

        code = FAKE_OTP

        OTPManager.add_otp_request(phone, code)

        return SUCCESS_RESPONSE

    @staticmethod
    async def verify_otp(db: AsyncSession, request: OTPVerifyRequest) -> AuthResponse:
        """Если код совпадает, проводим авторизацию"""
        phone = request.phone
        otp = request.otp
        if not OTPManager.verify(phone_number=phone, code=otp):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Неверный или просроченный код подтверждения"
            )
        user: UserBase = await UserBase.get_by_phone(phone, session=db)

        if user is None:
            new_user = UserBase(
                name=None,
                encrypted_phone=OTPManager.encrypt_phone_number(phone)
            )
            await new_user.create(db)
            await db.commit()
            user = new_user  # Чтобы получить uuid
            username = None
        else:
            username = user.name

        # UUID input should be a string, bytes or UUID object
        # [type=uuid_type, input_value=UUID('...'), input_type=UUID]
        # Поэтому просто uuid_utils.uuid7() не воркает -> оборачиваем в str
        token = str(uuid_utils.uuid7())
        token_base = TokenBase(token=token, user_id=user.id)

        await token_base.upsert(db)
        await db.commit()

        return AuthResponse(
            user_id=str(user.id),
            token=token,
            name=username
        )

    @staticmethod
    async def register_user(db: AsyncSession, user: UserBase, request: UserRegistrationRequest):
        name = request.name
        telegram = request.telegram
        new_user = UserBase(
            id=user.id,  # по айди понимает, что мы меняем =)
            name=name,
            telegram_username=telegram
        )
        await UserBase.update(
            new_user, session=db
        )
        await db.commit()

        return SUCCESS_RESPONSE
