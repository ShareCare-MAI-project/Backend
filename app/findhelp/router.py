import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.findhelp.schemas import FindHelpBasicResponse
from app.findhelp.service import FindHelpService
from app.user.user_base import UserBase
from app.utils.decorators.handle_errors import handle_errors
from app.utils.di.get_current_user import get_current_user
from app.findhelp.schemas import TakeItemResponse
from app.common.schemas import SearchRequest
from app.items.schemas import ItemResponse

router = APIRouter()


@router.get("/basic", response_model=FindHelpBasicResponse)
@handle_errors()
async def get_findhelp_basic_items(
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user)
):
    return await FindHelpService.get_findhelp_basic_items(db, user_id=user.id)


@router.post("/search", response_model=list[ItemResponse])
@handle_errors()
async def search(
        request: SearchRequest,
        db: AsyncSession = Depends(get_async_db)
):
    return await FindHelpService.search_items(db, request)


@router.patch("/take/{item_id}", response_model=TakeItemResponse)
@handle_errors()
async def take_item(
        item_id: uuid.UUID,
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user)
):
    return await FindHelpService.take_item(db, user_id=user.id, item_id=item_id)
