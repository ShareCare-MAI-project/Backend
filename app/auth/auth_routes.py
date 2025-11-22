import logging

from fastapi import APIRouter, HTTPException
from starlette import status

from app.auth.auth_models import LoginRequest, AuthResponse, OTPVerifyRequest
from app.auth.auth_service import AuthService

router = APIRouter()

TAG = "Auth"


@router.post(
    "/auth/request-otp",
    status_code=status.HTTP_200_OK,
    summary="Запросить OTP-код для входа",
    description="Отправить 4-значный код подтверждения на номер телефона",
    tags=[TAG]
)
async def login(request: LoginRequest):
    try:
        return await AuthService.request_otp(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при отправке кода"
        )


@router.post(
    "/auth/verify-otp",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Войти с OTP кодом",
    description="Подтвердить номер телефона с помощью OTP кода и получить токен",
    tags=[TAG]
)
async def verify_otp(request: OTPVerifyRequest):
    try:
        return await AuthService.verify_otp(request)
    except HTTPException:
        # Перебрасываем уже обработанные ошибки
        raise
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при верификации кода"
        )
