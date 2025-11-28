import uuid

from app.items.enums import ItemStatus, ItemDelivery
from app.requests.models import RequestBase, RequestDeliveryTypeBase
from app.requests.schemas import Request


# noinspection PyPep8Naming
def Requests_to_RequestBase(request: Request,
                            user_id: uuid.UUID,
                            request_id: uuid.UUID | None = None,
                            status: ItemStatus = ItemStatus.listed
                            ) -> RequestBase:
    return RequestBase(
        id=request_id,
        user_id=user_id,
        text=request.text,
        location=request.location,
        category=request.category,
        status=status,
    )


# noinspection PyPep8Naming
def RequestDelivery_to_RequestDeliveryTypeBase(
        delivery: ItemDelivery,
        request_id: uuid.UUID,
        id: uuid.UUID | None = None,
) -> RequestDeliveryTypeBase:
    return RequestDeliveryTypeBase(
        id=id,
        request_id=request_id,
        delivery_type=delivery
    )
