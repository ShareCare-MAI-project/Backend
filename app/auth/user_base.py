from enum import Enum
from typing import Optional

from sqlalchemy import String, LargeBinary, Integer, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.core.database import Base


class VerificationStatus(Enum):
    """Статус верификации организации"""
    PENDING = "pending"          # Ожидает проверки
    APPROVED = "approved"        # Одобрено
    REJECTED = "rejected"        # Отклонено


class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    encrypted_phone: Mapped[bytes] = mapped_column(LargeBinary, unique=True)
    
    # Поля для организаций
    is_organization: Mapped[bool] = mapped_column(Boolean, default=False)
    organization_verification_status: Mapped[Optional[str]] = mapped_column(
        String(20),
        default=VerificationStatus.PENDING.value,
        nullable=True
    )

    def __repr__(self) -> str:
        return f"UserBase(id={self.id}, name={self.name}, is_organization={self.is_organization})"

    @staticmethod
    async def update(new_object: 'UserBase', session):
        """Обновить пользователя в БД"""
        session.merge(new_object)

    @staticmethod
    async def create_user(session, phone: str, name: Optional[str] = None, is_organization: bool = False):
        """Создать нового пользователя"""
        from app.auth.utils.phone_number import PhoneNumber
        encrypted_phone = PhoneNumber.encrypt(phone)
        
        user = UserBase(
            name=name,
            encrypted_phone=encrypted_phone,
            is_organization=is_organization,
            organization_verification_status=VerificationStatus.PENDING.value if is_organization else None
        )
        session.add(user)
        await session.commit()
        return user