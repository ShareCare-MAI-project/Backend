from fastapi import APIRouter, Depends, Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.user_schemas import UserFullInfoResponse, QuickInfoResponse
from app.utils.decorators.handle_errors import handle_errors
from app.user.user_service import UserService
from app.user.user_base import UserBase
from app.utils.di.get_current_user import get_current_user
from app.core.database import get_async_db
from uuid import UUID
router = APIRouter()


@router.get(
    path="/me",
    response_model=UserFullInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о текущем пользователе",
    description="Возвращает данные пользователя по токену, проверяет его валидность"
)
@handle_errors(error_message="Ошибка при получении данных о пользователе")
async def get_current_user_info(
    user: UserBase = Depends(get_current_user)
):
    return await UserService.get_user_full_info(user)


@router.get(
    path="/quick-info",
    response_model=QuickInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить быструю информацию пользователя"
)
@handle_errors(error_message="Ошибка при получении данных о пользователе")
async def get_quick_info(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db),
):
    result = await UserService().get_QuickInfo(user_id, db)
    return QuickInfoResponse(**result)
