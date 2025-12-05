from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.user.user_schemas import UserFullInfoResponse
from app.utils.decorators.handle_errors import handle_errors
from app.user.user_service import UserService
from app.user.user_base import UserBase
from app.utils.di.get_current_user import get_current_user
from app.core.database import get_async_db

router = APIRouter()


@router.get(
    path="/me",
    response_model=UserFullInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о текущем пользователе (для обновления данных о нём при запуске приложения)",
    description="Возвращает данные пользователя по токену, проверяет его валидность"
)
@handle_errors(error_message="Ошибка при получении данных о пользователе")
async def get_current_user_info(
        user: UserBase = Depends(get_current_user)
):
    return await UserService.get_user_full_info(user)


@router.post(
    path="/verification",
    status_code=status.HTTP_200_OK,
)
@handle_errors(error_message="Ошибка при получении данных о пользователе")
async def update_verification(
        verified: bool,
        organization_name: str | None = None,
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user),

):
    return await UserService.update_verification(db=db,user=user,verified=verified,organization_name=organization_name)