from pydantic import BaseModel

from app.requests.schemas import RequestResponse
from app.items.schemas import ItemTelegramResponse


class FindHelpBasicResponse(BaseModel):
    ready_to_help: list[ItemTelegramResponse]
    my_requests: list[RequestResponse]


class TakeItemResponse(BaseModel):
    telegram: str
