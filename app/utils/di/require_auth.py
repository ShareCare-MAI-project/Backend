import asyncio
import uuid
from functools import wraps

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.token_base import TokenBase
from app.core.database import get_async_db

security = HTTPBearer()


# Было бы неплохо переписать как декоратор, но выходит ошибка, что security нет в Depends =(
async def require_auth(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_async_db)
):
    """Не даёт мёртвому токену выполнять запросы"""
    token = uuid.UUID(credentials.credentials)
    user_id = await TokenBase.get_user_id_by_token(token, db)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return user_id
