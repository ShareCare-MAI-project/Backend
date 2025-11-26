import json
from uuid import UUID

from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.items.schemas import ItemResponse, Item
from app.items.service import ItemsService
from app.user.user_base import UserBase
from app.utils.decorators.handle_errors import handle_errors
from app.utils.di.get_current_user import get_current_user
from app.utils.di.require_auth import require_auth

router = APIRouter()


@router.get("/", response_model=list[ItemResponse])
@handle_errors()
async def get_items(
        db: AsyncSession = Depends(get_async_db),
        _=Depends(require_auth)
):
    return await ItemsService.get_items(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
@handle_errors()
async def create_item(
        item_data: str = Form(..., description="JSONчик от item data (отправляем formData с мобилки)"),
        images: list[UploadFile] = File(),
        db: AsyncSession = Depends(get_async_db),
        user: UserBase = Depends(get_current_user),
        # _=Depends(require_auth) Не нужно, т.к. выше мы получаем пользователя
):
    item_dict = json.loads(item_data)
    item = Item(**item_dict)
    return await ItemsService.create_item(
        db, item=item, images=images, owner_id=user.id
    )


@router.get("/{item_id}", response_model=ItemResponse)
@handle_errors()
async def get_item(
        item_id: UUID,
        db: AsyncSession = Depends(get_async_db),
        _=Depends(require_auth)
):
    return await ItemsService.get_item(db, item_id)

# @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
# @handle_errors()
# def remove_item(item_id: UUID, db: AsyncSession = Depends(get_async_db)):
#     success = delete_item(db, item_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="товар не найден")
#     return
#
#
# @router.patch("/{item_id}", response_model=ItemResponse)
# @handle_errors()
# def update_item(item_id: UUID, item_update: ItemUpdate, db: AsyncSession = Depends(get_async_db)):
#     item = update_item(db, item_id, item_update)
#     if not item:
#         raise HTTPException(status_code=404, detail="товар не найден")
#     return item
#
#
# @router.post("/{item_id}/reserve", response_model=ItemResponse)
# @handle_errors()
# def reserve_item(item_id: UUID, recipient_id: UUID, db: AsyncSession = Depends(get_async_db)):
#     item = reserve_item(db, item_id, recipient_id)
#     if not item:
#         raise HTTPException(status_code=400, detail="не найден или зарезервирован")
#     return item
#
#
# @router.post("/{item_id}/close", response_model=ItemResponse)
# @handle_errors()
# def close_item(item_id: UUID, db: AsyncSession = Depends(get_async_db)):
#     item = close_item(db, item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="товар найден")
#     return item
