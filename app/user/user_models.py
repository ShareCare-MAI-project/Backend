from typing import Optional
from pydantic import BaseModel, Field, UUID7
from app.auth.utils.phone_number import PhoneNumber


class UserFullInfoResponse(BaseModel):
    phone: PhoneNumber
    name: str = Field(max_length=20, examples=["Артём"], description="Имя пользователя")
    telegram_username: str = Field(min_length=5, max_length=32,
                                   description="Телеграм (username) пользователя; Храним БЕЗ собаки")
    is_verified: bool = Field(description="Подтверждён аккаунт или нет")
    organization_name: Optional[str] = Field(None, max_length=40,
                                             description="Название организации (если есть)")
