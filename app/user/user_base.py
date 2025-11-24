import uuid
from typing import Optional

import uuid_utils
from sqlalchemy import String, select, LargeBinary, UUID, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.auth.utils.otp_manager import OTPManager
from app.auth.utils.phone_number import PhoneNumber
from app.core.database import Base


class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=lambda: uuid_utils.uuid7(),
        unique=True,
        nullable=False
    )
    encrypted_phone: Mapped[bytes] = mapped_column(LargeBinary, unique=True)

    # Optional, т.к. во время регистрации у пользователя может не быть имени
    # Но это MVP момент, чтобы было меньше ручек =)
    name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    telegram_username: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)  # unique=True нет, т.к. MVP

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    organization_name: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)

    def __repr__(self) -> str:
        return f"UserBase(id={self.id}, name={self.name}, encrypted_phone={self.encrypted_phone})"

    @staticmethod
    async def update(new_object: 'UserBase', session: AsyncSession):
        await session.merge(new_object)

    async def create(self, session: AsyncSession):
        session.add(self)

    @classmethod
    async def get_by_phone(cls, phone: PhoneNumber, session) -> 'UserBase':
        """
        :return: МОЖЕТ ВЕРНУТЬ None!!! (не могу указать, т.к. питон...)
        """
        statement = select(UserBase).where(UserBase.encrypted_phone == OTPManager.encrypt_phone_number(phone))
        return (await session.scalars(statement)).one_or_none()

    @classmethod
    async def get_by_id(cls, user_id: uuid.UUID, session: AsyncSession) -> 'UserBase':
        """
        :return: МОЖЕТ ВЕРНУТЬ None!!! (не могу указать, т.к. питон...)
        """
        stmt = select(UserBase).where(UserBase.id == user_id)
        return (await session.scalars(stmt)).one_or_none()
