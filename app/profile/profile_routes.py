from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.auth.auth_models import (
    ProfileUpdateRequest, ProfileResponse, 
    OrganizationVerificationRequest, AdminVerificationRequest
)
from app.auth.user_base import UserBase, VerificationStatus
from app.core.database import default_async_db_request, get_db

router = APIRouter()

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(db: Session = Depends(get_db)):
    """Получить профиль текущего пользователя"""
    user = db.query(UserBase).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return user

@router.put("/profile", response_model=ProfileResponse)
async def update_profile(
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db)
):
    """Обновить профиль пользователя"""
    user = db.query(UserBase).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if request.name is not None:
        user.name = request.name
    
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/organization/request-verification")
async def request_organization_verification(
    request: OrganizationVerificationRequest,
    db: Session = Depends(get_db)
):
    """Пользователь подаёт заявку на верификацию организации"""
    user = db.query(UserBase).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Проверяем, не подавал ли уже заявку
    if user.organization_verification_status == VerificationStatus.PENDING:
        raise HTTPException(
            status_code=400, 
            detail="У вас уже есть активная заявка на верификацию"
        )
    
    if user.organization_verification_status == VerificationStatus.APPROVED:
        raise HTTPException(
            status_code=400,
            detail="Вы уже верифицированная организация"
        )
    
    # Обновляем данные организации
    user.is_organization = True
    user.organization_name = request.organization_name
    user.organization_description = request.organization_description
    user.organization_verification_status = VerificationStatus.PENDING
    user.verification_requested_at = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    
    return {
        "status": "success",
        "message": "Заявка отправлена на рассмотрение администратору",
        "organization_name": user.organization_name,
        "verification_status": user.organization_verification_status
    }

@router.get("/organization/verification-status")
async def get_verification_status(db: Session = Depends(get_db)):
    """Проверить статус верификации"""
    user = db.query(UserBase).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return {
        "is_organization": user.is_organization,
        "organization_name": user.organization_name,
        "verification_status": user.organization_verification_status,
        "can_receive_unlimited": (
            user.organization_verification_status == VerificationStatus.APPROVED
        ),
        "requested_at": user.verification_requested_at,
        "approved_at": user.verification_approved_at
    }

# ============ АДМИНСКИЕ ЭНДПОИНТЫ ============

@router.get("/admin/pending-verifications")
async def get_pending_verifications(db: Session = Depends(get_db)):
    """Админ: получить список заявок на верификацию"""
    # TODO: проверить, что это админ (через токен)
    
    pending_users = db.query(UserBase).filter(
        UserBase.organization_verification_status == VerificationStatus.PENDING
    ).all()
    
    return [
        {
            "user_id": user.id,
            "phone": user.encrypted_phone,
            "name": user.name,
            "organization_name": user.organization_name,
            "organization_description": user.organization_description,
            "requested_at": user.verification_requested_at
        }
        for user in pending_users
    ]

@router.post("/admin/verify-organization")
async def verify_organization(
    request: AdminVerificationRequest,
    db: Session = Depends(get_db)
):
    """Админ: одобрить или отклонить заявку"""
    # TODO: проверить, что это админ (через токен)
    
    user = db.query(UserBase).filter(UserBase.id == request.user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if request.approved:
        user.organization_verification_status = VerificationStatus.APPROVED
        user.verification_approved_at = datetime.utcnow()
        message = f"Организация '{user.organization_name}' одобрена! Теперь вы можете получать неограниченное количество вещей."
    else:
        user.organization_verification_status = VerificationStatus.REJECTED
        message = f"Заявка отклонена. Причина: {request.rejection_reason or 'не указана'}"
    
    db.commit()
    
    return {
        "status": "success",
        "message": message,
        "user_id": user.id,
        "verification_status": user.organization_verification_status
    }

@router.post("/admin/reject-organization")
async def reject_organization(
    user_id: int,
    reason: str,
    db: Session = Depends(get_db)
):
    """Админ: отклонить заявку"""
    # TODO: проверить, что это админ
    
    user = db.query(UserBase).filter(UserBase.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user.organization_verification_status = VerificationStatus.REJECTED
    # Можно добавить поле reason в БД если нужно хранить причины
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Заявка '{user.organization_name}' отклонена",
        "reason": reason
    }