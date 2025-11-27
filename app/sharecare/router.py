from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.sharecare.schemas import ShareCareItemsResponse
from app.utils.decorators.handle_errors import handle_errors
from app.core.database import get_async_db
from app.utils.di.get_current_user import get_current_user
from app.sharecare.service import ShareCareService
from app.user.user_base import UserBase

router = APIRouter()


@router.get("/items", response_model=ShareCareItemsResponse)
@handle_errors()
async def get_sharecare_items(
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user)
):
    return await ShareCareService.get_sharecare_items(db, user_id=user.id)
