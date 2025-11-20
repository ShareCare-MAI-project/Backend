from fastapi import APIRouter
from app.models import NeedRequest
import uuid
from datetime import datetime , timezone

router = APIRouter()

needs = {}

@router.post("")
async def create_need(data: NeedRequest):
    need_id = str(uuid.uuid4())
    needs[need_id] = {
        "id": need_id,
        "title": data.title,
        "category": data.category,
        "description": data.description,
        "size": data.size,
        "gender": data.gender,
        "urgent": data.urgent,
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return {"id": need_id}

@router.get("")
async def list_all_needs():
    return list(needs.values())

@router.delete("/{need_id}")
async def delete_need(need_id: str):
    if need_id in needs:
        del needs[need_id]
        return {"ok": True}
    return {"error": "Не найдено"}