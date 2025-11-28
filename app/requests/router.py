from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.utils.decorators.handle_errors import handle_errors
from app.requests.schemas import Request
from app.core.database import get_async_db
from app.utils.di.get_current_user import get_current_user
from app.user.user_base import UserBase
from app.requests.service import RequestService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
@handle_errors()
async def create_item(
        request: Request,
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user),
        # _=Depends(require_auth) Не нужно, т.к. выше мы получаем пользователя
):
    return await RequestService.create_item(db, request, user.id)
