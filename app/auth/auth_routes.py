import logging

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.auth.auth_models import LoginRequest, AuthResponse, OTPVerifyRequest
from app.auth.auth_service import AuthService
from app.auth.user_base import VerificationStatus
from app.core.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)
TAG = "Auth"


@router.post(
    "/request-otp",
    status_code=status.HTTP_200_OK,
    summary="Запросить OTP-код для входа",
    description="Отправить 4-значный код подтверждения на номер телефона",
    tags=[TAG]
)
async def login(request: LoginRequest):
    """Запросить OTP код для входа"""
    try:
        return await AuthService.request_otp(request)
    except Exception as e:
        logger.error(f"Ошибка при отправке OTP: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при отправке кода"
        )


@router.post(
    "/verify-otp",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Войти с OTP кодом",
    description="Подтвердить номер телефона с помощью OTP кода и получить токен",
    tags=[TAG]
)
async def verify_otp(request: OTPVerifyRequest):
    """Подтвердить OTP и получить токен авторизации"""
    try:
        return await AuthService.verify_otp(request)
    except Exception as e:
        logger.error(f"Ошибка при проверке OTP: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный код или номер телефона"
        )


@router.post(
    "/verify-organization",
    summary="Отправить запрос на верификацию организации",
    description="Организация отправляет документы для верификации",
    tags=[TAG]
)
async def request_organization_verification(
    documents: dict,
    db: Session = Depends(get_db)
):
    """
    Запрос на верификацию организации.
    
    Ожидается JSON с документами:
    {
        "org_name": "Название организации",
        "inn": "ИНН",
        "documents_url": "URL документов"
    }
    """
    try:
        # TODO: Реализовать логику верификации организации
        return {
            "status": "pending",
            "message": "Запрос на верификацию отправлен администратору"
        }
    except Exception as e:
        logger.error(f"Ошибка при верификации организации: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при отправке запроса на верификацию"
        )


@router.get(
    "/me",
    response_model=dict,
    summary="Получить информацию о текущем пользователе",
    tags=[TAG]
)
async def get_current_user(
    db: Session = Depends(get_db)
):
    """
    Получить данные текущего авторизованного пользователя.
    
    Требует валидный JWT токен в заголовке Authorization.
    """
    try:
        # TODO: Получить пользователя из токена и вернуть его данные
        return {
            "id": 1,
            "name": "John Doe",
            "is_organization": False,
            "organization_verification_status": None
        }
    except Exception as e:
        logger.error(f"Ошибка при получении пользователя: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неавторизованный доступ"
        )