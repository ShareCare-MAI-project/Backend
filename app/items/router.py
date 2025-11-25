from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.items.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.items.crud import get_item, create_item, get_item, delete_item, update_item, reserve_item, close_item
from app.core.database import get_db  

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return get_item(db)

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: UUID, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="товар не найден")
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(item_id: UUID, db: Session = Depends(get_db)):
    success = delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="товар не найден")
    return

@router.patch("/{item_id}", response_model=ItemResponse)
def update__item(item_id: UUID, item_update: ItemUpdate, db: Session = Depends(get_db)):
    item = update_item(db, item_id, item_update)
    if not item:
        raise HTTPException(status_code=404, detail="товар не найден")
    return item

@router.post("/{item_id}/reserve", response_model=ItemResponse)
def reserve__item(item_id: UUID, recipient_id: UUID, db: Session = Depends(get_db)):
    item = reserve_item(db, item_id, recipient_id)
    if not item:
        raise HTTPException(status_code=400, detail="не найден или зарезервирован")
    return item

@router.post("/{item_id}/close", response_model=ItemResponse)
def close__item(item_id: UUID, db: Session = Depends(get_db)):
    item = close_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="товар найден")
    return item