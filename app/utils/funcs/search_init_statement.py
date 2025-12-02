from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.items.enums import ItemCategory, ItemDelivery, ItemStatus
from app.items.models import ItemBase, ItemDeliveryTypeBase
from app.requests.models import RequestBase, RequestDeliveryTypeBase


def search_init_statement(base: type[ItemBase] | type[RequestBase],
                          delivery_base: type[RequestDeliveryTypeBase] | type[ItemDeliveryTypeBase],
                          category: ItemCategory | None, delivery_types: list[ItemDelivery]):
    delivery_types = delivery_types if delivery_types else list(ItemDelivery)

    if base == ItemBase:
        stmt = select(base).options(
            selectinload(ItemBase.delivery_bases),
            selectinload(ItemBase.image_bases) # чтоб не крашило
        )
    else:
        stmt = select(base).options(
            selectinload(RequestBase.delivery_bases)
        )

    stmt = stmt.where(
        base.status == ItemStatus.listed,
        base.delivery_bases.any(
            delivery_base.delivery_type.in_(delivery_types)
        )
    )

    if category is not None:
        stmt = stmt.where(base.category == category)
    return stmt
