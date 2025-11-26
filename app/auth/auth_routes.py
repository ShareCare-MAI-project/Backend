from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.auth_schemas import LoginRequest, AuthResponse, OTPVerifyRequest, UserRegistrationRequest
from app.auth.auth_service import AuthService
from app.utils.decorators.handle_errors import handle_errors
from app.user.user_base import UserBase
from app.utils.di.get_current_user import get_current_user
from app.core.database import get_async_db

router = APIRouter()


@router.post(
    "/request-otp",
    status_code=status.HTTP_200_OK,
    summary="Запросить OTP-код для входа",
    description="Отправить 4-значный код подтверждения на номер телефона"
)
@handle_errors(error_message="Ошибка при отправке кода")
async def login(
        request: LoginRequest,
):
    return await AuthService.request_otp(request)


@router.post(
    "/verify-otp",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Войти с OTP кодом",
    description="Подтвердить номер телефона с помощью OTP кода и получить токен"
)
@handle_errors(error_message="Ошибка при верификации кода")
async def verify_otp(
        request: OTPVerifyRequest,
        db: AsyncSession = Depends(get_async_db)
):
    return await AuthService.verify_otp(db, request)


@router.post(
    "/registration",
    status_code=status.HTTP_200_OK,
    summary="Зарегистрировать пользователя",
    description="Добавить в БД имя и телеграм (уже есть токен и айди)"
)
@handle_errors(error_message="Ошибка при регистрации пользователя")
async def register_user(
        request: UserRegistrationRequest,
        user: UserBase = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)
):
    return await AuthService.register_user(db, user, request)
