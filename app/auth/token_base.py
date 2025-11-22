from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped
import uuid

from app.core.database import Base


class TokenBase(Base):
    __tablename__ = "tokens"

    token: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        unique=True,
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        unique=True,
        nullable=False
    )

    async def upsert(self, session: AsyncSession):
        stmt = insert(TokenBase).values(
            token=self.token,
            user_id=self.user_id
        ).on_conflict_do_update(
            index_elements=['user_id'],
            set_=dict(token=self.token)
        )
        await session.execute(stmt)
