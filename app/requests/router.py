import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.utils.decorators.handle_errors import handle_errors
from app.requests.schemas import Request
from app.core.database import get_async_db
from app.utils.di.get_current_user import get_current_user
from app.user.user_base import UserBase
from app.requests.service import RequestService
from app.requests.schemas import RequestWithId
from app.common.schemas import ItemQuickInfoResponse

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
@handle_errors()
async def create_request(
        request: Request,
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user),
        # _=Depends(require_auth) Не нужно, т.к. выше мы получаем пользователя
):
    return await RequestService.create_reqeust(db, request, user.id)


@router.patch("/", status_code=status.HTTP_200_OK)
@handle_errors()
async def edit_request(
        request: RequestWithId,
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user)
):
    return await RequestService.edit_request(db, request, user_id=user.id)


@router.delete("/", status_code=status.HTTP_200_OK)
@handle_errors()
async def delete_request(
        request_id: uuid.UUID,
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user)
):
    return await RequestService.delete_request(db, request_id=request_id, user_id=user.id)


@router.get("/quick-info/{request_id}", response_model=ItemQuickInfoResponse)
@handle_errors()
async def get_item_quick_info(
        request_id: uuid.UUID,
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user)
):
    return await RequestService.get_request_quick_info(db, request_id=request_id, user_id=user.id)
