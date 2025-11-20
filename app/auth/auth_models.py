from pydantic import BaseModel
from typing import Optional
from enum import Enum

class VerificationStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LoginRequest(BaseModel):
    phone: str

class OTPVerifyRequest(BaseModel):
    phone: str
    otp: str

class AuthResponse(BaseModel):
    token: str
    name: Optional[str] = None

class OrganizationVerificationRequest(BaseModel):
    """Запрос на верификацию организации"""
    organization_name: str
    organization_description: str
    # Опционально: можно добавить документы, ссылку на сайт и т.д.

class ProfileUpdateRequest(BaseModel):
    """Для обновления профиля пользователя"""
    name: Optional[str] = None
    is_organization: Optional[bool] = None

class ProfileResponse(BaseModel):
    """Ответ с профилем пользователя"""
    id: int
    name: Optional[str]
    encrypted_phone: str
    is_organization: bool
    organization_name: Optional[str]
    organization_description: Optional[str]
    organization_verification_status: Optional[VerificationStatusEnum]
    created_at: str
    
    class Config:
        from_attributes = True

class AdminVerificationRequest(BaseModel):
    """Для админа - одобрить/отклонить организацию"""
    user_id: int
    approved: bool
    rejection_reason: Optional[str] = None