from pydantic import BaseModel
from typing import Optional, List

class AuthRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    code: str

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    telegram: Optional[str] = None
    is_organization: Optional[bool] = False        
    organization_name: Optional[str] = None        

class Item(BaseModel):
    title: str
    category: str
    location: str
    description: Optional[str] = None
    size: Optional[str] = None
    gender: Optional[str] = None
    condition: str = "good"
    photos: List[str] = []

class RequestForItem(BaseModel):
    requester_name: Optional[str] = None
    requester_telegram: Optional[str] = None

class NeedRequest(BaseModel):
    title: str
    category: str
    description: Optional[str] = None
    size: Optional[str] = None
    gender: Optional[str] = None
    urgent: bool = False