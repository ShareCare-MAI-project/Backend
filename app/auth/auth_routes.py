from fastapi import APIRouter, Depends
from starlette import status

from app.auth.auth_models import LoginRequest, AuthResponse, OTPVerifyRequest, UserRegistrationRequest
from app.auth.auth_service import AuthService
from app.utils.handle_errors import handle_errors
from app.auth.user_base import UserBase
from app.utils.get_current_user import get_current_user

router = APIRouter()

TAG = "Auth"


@router.post(
    "/auth/request-otp",
    status_code=status.HTTP_200_OK,
    summary="Запросить OTP-код для входа",
    description="Отправить 4-значный код подтверждения на номер телефона",
    tags=[TAG]
)
@handle_errors(error_message="Ошибка при отправке кода")
async def login(request: LoginRequest):
    return await AuthService.request_otp(request)


@router.post(
    "/auth/verify-otp",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Войти с OTP кодом",
    description="Подтвердить номер телефона с помощью OTP кода и получить токен",
    tags=[TAG]
)
@handle_errors(error_message="Ошибка при верификации кода")
async def verify_otp(request: OTPVerifyRequest):
    return await AuthService.verify_otp(request)


@router.post(
    "/auth/registration",
    status_code=status.HTTP_200_OK,
    summary="Зарегистрировать пользователя",
    description="Добавить в БД имя и телеграм (уже есть токен и айди)",
    tags=[TAG]
)
@handle_errors(error_message="Ошибка при регистрации пользователя")
async def register_user(
        request: UserRegistrationRequest,
        user: UserBase = Depends(get_current_user)
):
    return await AuthService.register_user(user, request)
