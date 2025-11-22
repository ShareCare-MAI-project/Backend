import uuid_utils
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.auth.auth_models import LoginRequest, OTPVerifyRequest, AuthResponse
from app.auth.user_base import UserBase
from app.auth.utils.otp_manager import OTPManager
from app.core.database import default_async_db_request
from app.auth.token_base import TokenBase

FAKE_OTP = "1111"


class AuthService:

    @staticmethod
    async def request_otp(request: LoginRequest) -> dict:
        """Отправить OTP код на телефон"""
        phone = request.phone

        code = FAKE_OTP

        OTPManager.add_otp_request(phone, code)

        return {"success": True}

    @staticmethod
    async def verify_otp(request: OTPVerifyRequest) -> AuthResponse:
        """Если код совпадает, проводим авторизацию"""
        phone = request.phone
        otp = request.otp
        if not OTPManager.verify(phone_number=phone, code=otp):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Неверный или просроченный код подтверждения"
            )
        user: UserBase = await default_async_db_request(lambda session: UserBase.get_by_phone(phone, session=session))

        if user is None:
            new_user = UserBase(
                name=None,
                encrypted_phone=OTPManager.encrypt_phone_number(phone)
            )
            await default_async_db_request(new_user.create)
            user = new_user  # Чтобы получить uuid
            username = None
        else:
            username = user.name

        # UUID input should be a string, bytes or UUID object
        # [type=uuid_type, input_value=UUID('...'), input_type=UUID]
        # Поэтому просто uuid_utils.uuid7() не воркает -> оборачиваем в str
        token = str(uuid_utils.uuid7())

        await default_async_db_request(TokenBase(token=token, user_id=user.id).upsert)

        return AuthResponse(
            token=token,
            name=username
        )
