from pydantic import BaseModel

from app.items.schemas import ItemResponse
from app.items.schemas import ItemTelegramResponse


class ShareCareItemsResponse(BaseModel):
    responses: list[ItemTelegramResponse]
    my_published_items: list[ItemResponse]


