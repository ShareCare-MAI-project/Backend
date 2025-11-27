from pydantic import BaseModel

from app.items.schemas import ItemResponse


class ShareCareItemsResponse(BaseModel):
    responses: list[ItemResponse]
    my_published_items: list[ItemResponse]
