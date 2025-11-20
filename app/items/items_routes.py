from fastapi import APIRouter, HTTPException, Depends
from app.models import Item, RequestForItem
from app.items.items_service import (
    create_item, get_item, list_items, 
    create_request_for_item, get_item_requests, 
    approve_request, count_items_this_month
)
from sqlalchemy.orm import Session
from app.auth.user_base import UserBase, VerificationStatus
from app.core.database import get_db

router = APIRouter()

@router.post("")
async def create_new_item(data: Item):
    item = create_item(data.dict(), donor_id="user123")
    return {"id": item["id"], "status": "created"}

@router.get("")
async def list_all_items(category: str = None):
    return list_items(category)

@router.get("/{item_id}")
async def get_item_detail(item_id: str):
    item = get_item(item_id)
    if not item:
        raise HTTPException(404, "Не найдено")
    return item

@router.post("/{item_id}/request")
async def request_for_item(item_id: str, data: RequestForItem):
    req = create_request_for_item(item_id, data.requester_name, data.requester_telegram)
    if not req:
        raise HTTPException(404, "Вещь не найдена")
    return {"id": req["id"], "status": "created"}

@router.get("/{item_id}/requests")
async def get_requests(item_id: str):
    reqs = get_item_requests(item_id)
    if reqs is None:
        raise HTTPException(404, "Вещь не найдена")
    return reqs

@router.post("/{item_id}/approve/{request_id}")
async def approve(item_id: str, request_id: str, db: Session = Depends(get_db)):
    req = approve_request(item_id, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Не найдено")
    
    # Получаем пользователя-получателя (пример)
    user = db.query(UserBase).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Проверка лимитов и верификации
    if not user.is_organization:
        items_count = count_items_this_month(user.items_received)
        if items_count >= 10:
            raise HTTPException(
                status_code=400,
                detail=f"Достигнут лимит: 10 вещей за месяц. Вы получили {items_count}"
            )
    else:
        if user.organization_verification_status != VerificationStatus.APPROVED:
            raise HTTPException(
                status_code=403,
                detail="Организация не верифицирована. Безлимит доступен только после подтверждения администратора"
            )

    return {
        "status": "approved",
        "message": "Вещь отдана",
        "requester_telegram": req["requester_telegram"],
        "is_organization": user.is_organization,
        "verification_status": user.organization_verification_status if user.is_organization else None
    }