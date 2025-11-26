import uuid

from app.items.enums import ItemDelivery, ItemStatus
from app.items.models import ItemBase
from app.items.schemas import ItemResponse, Item


# noinspection PyPep8Naming
def ItemBase_to_ItemResponse(item: ItemBase, delivery_types: list[ItemDelivery], images: list[str]) -> ItemResponse:
    return ItemResponse(
        title=item.title,
        description=item.description,
        location=item.location,
        category=item.category,
        delivery_types=delivery_types,
        id=item.id,
        owner=item.owner_id,
        recipient=item.recipient_id,
        images=images
    )


# noinspection PyPep8Naming
def Item_to_ItemBase(item: Item,
                     owner_id: uuid.UUID,
                     item_id: uuid.UUID | None = None,
                     recipient_id: uuid.UUID | None = None,
                     status: ItemStatus = ItemStatus.listed
                     ) -> ItemBase:
    return ItemBase(
        id=item_id,
        owner_id=owner_id,
        recipient_id=recipient_id,
        title=item.title,
        description=item.description,
        location=item.location,
        category=item.category,
        status=status
    )
