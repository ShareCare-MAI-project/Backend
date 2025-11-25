from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List

from .models import Item
from .schemas import ItemCreate, ItemUpdate


def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: UUID) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(Item).offset(skip).limit(limit).all()


def update_item(db: Session, item_id: UUID, item_update: ItemUpdate) -> Optional[Item]:
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: UUID) -> bool:
    db_item = get_item(db, item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True


def reserve_item(db: Session, item_id: UUID, recipient_id: UUID) -> Optional[Item]:
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    db_item.recipient = recipient_id
    db_item.status = "выбран получатель"
    db.commit()
    db.refresh(db_item)
    return db_item


def close_item(db: Session, item_id: UUID) -> Optional[Item]:
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    db_item.status = "закрыто"
    db.commit()
    db.refresh(db_item)
    return db_item
