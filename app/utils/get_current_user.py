import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.token_base import TokenBase
from app.auth.user_base import UserBase
from app.core.database import default_async_db_request

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserBase:
    token = uuid.UUID(credentials.credentials)

    user_id = await default_async_db_request(
        lambda session: TokenBase.get_user_id_by_token(token, session)
    )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = await default_async_db_request(
        lambda session: UserBase.get_by_id(user_id, session)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
