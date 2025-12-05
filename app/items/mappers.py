import uuid

from app.items.enums import ItemDelivery, ItemStatus
from app.items.models import ItemBase, ItemImageBase
from app.items.models import ItemDeliveryTypeBase
from app.items.schemas import ItemResponse, Item
from app.items.schemas import ItemTelegramResponse
from app.items.schemas import ItemCreateRequest
from app.items.schemas import TransactionResponse
from app.utils.funcs.datetime_to_str_date import datetime_to_str_date


# noinspection PyPep8Naming
def ItemBase_to_ItemResponse(item: ItemBase) -> ItemResponse:
    return ItemResponse(
        title=item.title,
        description=item.description,
        location=item.location,
        category=item.category,
        delivery_types=deliveries_bases_to_deliveries(item.delivery_bases),
        id=item.id,
        owner=item.owner_id,
        recipient=item.recipient_id,
        images=image_bases_to_images_links(item.image_bases)
    )


# noinspection PyPep8Naming
def ItemBase_to_ItemTelegramResponse(item: ItemBase, telegram: str) -> ItemTelegramResponse:
    return ItemTelegramResponse(
        title=item.title,
        description=item.description,
        location=item.location,
        category=item.category,
        delivery_types=deliveries_bases_to_deliveries(item.delivery_bases),
        id=item.id,
        owner=item.owner_id,
        recipient=item.recipient_id,
        images=image_bases_to_images_links(item.image_bases),
        telegram=telegram
    )


# noinspection PyPep8Naming
def ItemRequest_to_ItemBase(item: ItemCreateRequest,
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
        status=status,
        request_id=item.request_id
    )


# noinspection PyPep8Naming
def ItemDelivery_to_ItemDeliveryTypeBase(
        item_delivery: ItemDelivery,
        item_id: uuid.UUID,
        id: uuid.UUID | None = None,
) -> ItemDeliveryTypeBase:
    return ItemDeliveryTypeBase(
        id=id,
        item_id=item_id,
        delivery_type=item_delivery
    )


# noinspection PyPep8Naming
def ItemBase_to_TransactionResponse(
        item_base: ItemBase,
        user_id: uuid.UUID
) -> TransactionResponse:
    return TransactionResponse(
        item_id=item_base.id,
        title=item_base.title,
        description=item_base.description,
        image_link=item_base.image_bases[0].image,
        is_recipient=item_base.recipient_id == user_id,
        date_of_receipt=datetime_to_str_date(item_base.edited_at)
    )


def item_bases_to_item_responses(item_bases: list[ItemBase]) -> list[ItemResponse]:
    return [ItemBase_to_ItemResponse(item_base) for item_base in item_bases]


def image_bases_to_images_links(image_bases: list[ItemImageBase]) -> list[str]:
    return [image_base.image for image_base in image_bases]


def deliveries_bases_to_deliveries(delivery_bases: list[ItemDeliveryTypeBase]) -> list[ItemDelivery]:
    return [item_base.delivery_type for item_base in delivery_bases]
