from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.findhelp.schemas import FindHelpBasicResponse
from app.user.user_base import UserBase
from app.utils.decorators.handle_errors import handle_errors
from app.utils.di.get_current_user import get_current_user
from app.findhelp.service import FindHelpService

router = APIRouter()


@router.get("/basic", response_model=FindHelpBasicResponse)
@handle_errors()
async def get_findhelp_basic_items(
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user)
):
    return await FindHelpService.get_findhelp_basic_items(db, user_id=user.id)