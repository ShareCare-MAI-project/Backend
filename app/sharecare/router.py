from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.sharecare.schemas import ShareCareItemsResponse
from app.utils.decorators.handle_errors import handle_errors
from app.core.database import get_async_db
from app.utils.di.get_current_user import get_current_user
from app.sharecare.service import ShareCareService
from app.user.user_base import UserBase
from app.common.schemas import SearchRequest
from app.requests.schemas import RequestResponse

router = APIRouter()


@router.get("/items", response_model=ShareCareItemsResponse)
@handle_errors()
async def get_sharecare_items(
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user)
):
    return await ShareCareService.get_sharecare_items(db, user_id=user.id)


@router.post("/search", response_model=list[RequestResponse])
@handle_errors()
async def search(
        request: SearchRequest,
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user)
):
    return await ShareCareService.search_requests(db, request, user_id=user.id)
